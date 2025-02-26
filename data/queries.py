# data/queries.py

import psycopg2
import pandas as pd
from config.db_config import DB_CONFIG

def fetch_table_stats():
    """Fetch table usage statistics from pg_stat_user_tables."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        query = """
            SELECT
                relname AS table_name,
                seq_scan,
                idx_scan,
                n_live_tup
            FROM pg_stat_user_tables;
        """
        df = pd.read_sql(query, conn)
        return df
    except Exception as e:
        print("Error fetching table stats:", e)
        return pd.DataFrame()
    finally:
        if 'conn' in locals() and conn:
            conn.close()

def fetch_table_sizes():
    """Fetch table sizes including total, table, and index sizes."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        query = """
            SELECT
                relname AS table_name,
                pg_total_relation_size(relid) AS total_size,
                pg_relation_size(relid) AS table_size,
                (pg_total_relation_size(relid) - pg_relation_size(relid)) AS index_size
            FROM pg_catalog.pg_statio_user_tables;
        """
        df = pd.read_sql(query, conn)
        return df
    except Exception as e:
        print("Error fetching table sizes:", e)
        return pd.DataFrame()
    finally:
        if 'conn' in locals() and conn:
            conn.close()

def fetch_index_usage():
    """Fetch index usage statistics by joining pg_stat_user_indexes with table info."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        query = """
            SELECT
                s.indexrelname AS index_name,
                t.relname AS table_name,
                s.idx_scan,
                pg_relation_size(s.indexrelid) AS index_size
            FROM pg_stat_user_indexes s
            JOIN pg_stat_user_tables t ON s.relid = t.relid;
        """
        df = pd.read_sql(query, conn)
        return df
    except Exception as e:
        print("Error fetching index usage:", e)
        return pd.DataFrame()
    finally:
        if 'conn' in locals() and conn:
            conn.close()

def fetch_slow_queries():
    """Fetch the top slow queries from pg_stat_statements."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        query = """
            SELECT query, calls, total_time, mean_time, rows
            FROM pg_stat_statements
            ORDER BY total_time DESC
            LIMIT 10;
        """
        df = pd.read_sql(query, conn)
        return df
    except Exception as e:
        print("Error fetching slow queries:", e)
        return pd.DataFrame()
    finally:
        if 'conn' in locals() and conn:
            conn.close()

def fetch_locks():
    """Fetch waiting locks by joining pg_locks with pg_stat_activity."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        query = """
            SELECT l.locktype, l.mode, l.granted, a.query, a.state, a.pid, a.usename, a.query_start
            FROM pg_locks l
            LEFT JOIN pg_stat_activity a ON l.pid = a.pid
            WHERE NOT l.granted;
        """
        df = pd.read_sql(query, conn)
        return df
    except Exception as e:
        print("Error fetching locks:", e)
        return pd.DataFrame()
    finally:
        if 'conn' in locals() and conn:
            conn.close()

def generate_recommendations():
    """Generate basic recommendations based on slow queries, locks, and table usage."""
    recommendations = []
    
    # Check for slow queries
    df_slow = fetch_slow_queries()
    if not df_slow.empty:
        top_slow = df_slow.iloc[0]
        # Use an arbitrary threshold (e.g., 500ms mean time)
        if top_slow['mean_time'] > 500:
            recommendations.append("Slow Query Detected: Consider optimizing or adding indexes for the query: '{}'...".format(top_slow['query'][:100]))
    
    # Check for waiting locks
    df_locks = fetch_locks()
    if not df_locks.empty:
        recommendations.append("There are {} waiting locks. Investigate long-running transactions.".format(len(df_locks)))
    
    # Check for tables with high sequential scans relative to index scans
    df_stats = fetch_table_stats()
    if not df_stats.empty:
        for _, row in df_stats.iterrows():
            if row['seq_scan'] > 10 * (row['idx_scan'] + 1):  # +1 to avoid division by zero
                recommendations.append("Table '{}' shows high sequential scans. Consider reviewing indexing strategy.".format(row['table_name']))
                break  # Limit to one recommendation per category
    
    if not recommendations:
        recommendations.append("No significant issues detected. Keep monitoring for anomalies.")
    
    return recommendations
