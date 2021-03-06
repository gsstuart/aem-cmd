# coding: utf-8
from StringIO import StringIO

from httmock import urlmatch, HTTMock
from mock import patch
from nose.tools import eq_

from acmd import tool_repo, Server


class MockHttpService(object):
    def __init__(self, asset_service=None):
        self.req_log = []
        self.url_log = []

    @urlmatch(netloc='localhost:4502')
    def __call__(self, url, request):
        self.req_log.append(request)
        self.url_log.append(url)
        return ""


@patch('sys.stdout', new_callable=StringIO)
@patch('sys.stderr', new_callable=StringIO)
def test_mv(stderr, stdout):
    service_mock = MockHttpService()
    with HTTMock(service_mock):
        tool = tool_repo.get_tool('mv')
        server = Server('localhost')
        status = tool.execute(server, ['mv', '/content/src_node', '/content/dst_node'])
        eq_(0, status)
        eq_('/content/dst_node\n', stdout.getvalue())
    eq_(1, len(service_mock.req_log))
    eq_('/content/src_node', service_mock.url_log[0].path)
    eq_('%3Aoperation=move&%3Adest=%2Fcontent%2Fdst_node', service_mock.req_log[0].body)


@patch('sys.stdout', new_callable=StringIO)
@patch('sys.stderr', new_callable=StringIO)
def test_mv_to_parent(stderr, stdout):
    service_mock = MockHttpService()
    with HTTMock(service_mock):
        tool = tool_repo.get_tool('mv')
        server = Server('localhost')
        status = tool.execute(server, ['mv', '/content/src_node', '/backup/'])
        eq_(0, status)
        eq_('/backup/src_node\n', stdout.getvalue())
    eq_(1, len(service_mock.req_log))
    eq_('/content/src_node', service_mock.url_log[0].path)
    eq_('%3Aoperation=move&%3Adest=%2Fbackup%2F', service_mock.req_log[0].body)
