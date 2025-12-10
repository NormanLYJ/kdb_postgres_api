from qpython import qconnection

class KDBClient:
    def __init__(self, host="localhost", port=5000, username=None, password=None):
        self.conn = qconnection.QConnection(
            host=host, port=port, username=username, password=password
        )
        self.conn.open()

    def query_transactions(self, start_date, end_date):
        # Example KDB query
        q = """
            select from trades 
            where time within (`date$"{sd}" ; `date$"{ed}")
        """.format(sd=start_date, ed=end_date)

        return self.conn(q)

    def close(self):
        self.conn.close()
