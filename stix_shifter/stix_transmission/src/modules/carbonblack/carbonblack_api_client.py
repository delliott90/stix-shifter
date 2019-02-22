from ..utils.RestApiClient import RestApiClient


class APIClient():
    PING_ENDPOINT = 'sensor'

    @staticmethod
    def _dialect_to_endpoint(dialect):
        assert dialect in ["binary", "process"]
        return dialect

    def __init__(self, connection, configuration):
        self.endpoint_start = 'api/v1/'
        auth = configuration.get('auth')
        headers = dict()
        headers['X-Auth-Token'] = auth.get('token')
        self.client = RestApiClient(connection.get('host'),
                                    connection.get('port'),
                                    connection.get('cert', None),
                                    headers,
                                    cert_verify=connection.get('cert_verify', 'True')
                                    )

    def ping_box(self):
        endpoint = self.endpoint_start + self.PING_ENDPOINT
        return self.client.call_api(endpoint, 'GET')

    def run_search(self, query_expression, dialect, start=0, rows=10):
        headers = dict()
        endpoint = self.endpoint_start + self._dialect_to_endpoint(dialect)
        data = [("q", query_expression), ("start", start), ("rows", rows)]

        # The purpose of this is to maintain order stability when doing paging
        if dialect == 'binary':
            sort_by = 'server_added_timestamp asc'
        else:  # process
            sort_by = 'start asc'
        data.append(("sort", sort_by))

        return self.client.call_api(endpoint, 'GET', headers, urldata=data)
