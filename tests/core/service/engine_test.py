# -*- coding: UTF-8 -*-

'''
Module
    engine_test.py
Info
    Unit tests for Service class.
'''

from __future__ import annotations

from collections.abc import Mapping, Sequence
import unittest

from ats_utilities.exceptions import ATSTypeError, ATSValueError

from testspeednet.core.model.speed_test_server import SpeedTestServer
from testspeednet.core.model.speed_test_stat import SpeedTestStat
from testspeednet.core.service.engine import Service


class MockSubProcessor:

    def __init__(self, init: bool = True, return_data: dict[str, object] | None = None) -> None:
        self._init = init
        self._return_data = return_data or {}

    def run(self, *, params: Mapping[str, object]) -> Mapping[str, object]:
        return self._return_data

    def is_initialized(self) -> bool:
        return self._init

    def __str__(self) -> str:
        return 'MockSubProcessor'


class MockServerRepository:

    def __init__(self, init: bool = True, servers: list[SpeedTestServer] | None = None) -> None:
        self._init = init
        self._servers = servers or []
        self.saved_servers: list[SpeedTestServer] = []
        self.saved_stats: list[SpeedTestStat] = []

    def get_servers(self) -> Sequence[SpeedTestServer]:
        return self._servers

    def save_servers(self, *, servers: Sequence[SpeedTestServer]) -> bool:
        self.saved_servers.extend(servers)
        return True

    def get_statistics(self, *, limit: int = 50) -> Sequence[SpeedTestStat]:
        return self.saved_stats[:limit]

    def save_statistic(self, *, stat: SpeedTestStat) -> bool:
        self.saved_stats.append(stat)
        return True

    def is_initialized(self) -> bool:
        return self._init

    def __str__(self) -> str:
        return 'MockServerRepository'


class MockJsonExporter:

    def __init__(self, init: bool = True) -> None:
        self._init = init
        self.exported_data: list[tuple[object, str]] = []

    def export_json(self, *, data: object, file_path: str) -> bool:
        self.exported_data.append((data, file_path))
        return True

    def load_json(self, *, file_path: str) -> dict[str, object]:
        return {'loaded': file_path}

    def is_initialized(self) -> bool:
        return self._init

    def __str__(self) -> str:
        return 'MockJsonExporter'


def create_sample_server(sid: int = 1) -> SpeedTestServer:
    return SpeedTestServer(
        id=sid,
        server_id=str(sid),
        url='http://sample.org',
        lat=45.0,
        lon=19.0,
        distance=10.0,
        name='TestCity',
        country='Serbia',
        cc='RS',
        sponsor='TestOrg',
        preferred=False,
        host='sample.org:8080'
    )


class TestService(unittest.TestCase):

    def test_init_success(self) -> None:
        svc = Service(
            subprocessor=MockSubProcessor(),
            server_repository=MockServerRepository(),
            json_exporter=MockJsonExporter()
        )
        self.assertTrue(svc.is_initialized())
        self.assertIn('Service', str(svc))

    def test_init_validation_failures(self) -> None:
        sub = MockSubProcessor()
        repo = MockServerRepository()
        exp = MockJsonExporter()

        with self.assertRaises((ATSValueError, ATSTypeError)):
            Service(subprocessor=None, server_repository=repo, json_exporter=exp)

        with self.assertRaises((ATSValueError, ATSTypeError)):
            Service(subprocessor='invalid', server_repository=repo, json_exporter=exp)

        with self.assertRaises((ATSValueError, ATSTypeError)):
            Service(subprocessor=sub, server_repository=None, json_exporter=exp)

        with self.assertRaises((ATSValueError, ATSTypeError)):
            Service(subprocessor=sub, server_repository='invalid', json_exporter=exp)

        with self.assertRaises((ATSValueError, ATSTypeError)):
            Service(subprocessor=sub, server_repository=repo, json_exporter=None)

        with self.assertRaises((ATSValueError, ATSTypeError)):
            Service(subprocessor=sub, server_repository=repo, json_exporter='invalid')

    def test_is_initialized_variations(self) -> None:
        svc1 = Service(
            subprocessor=MockSubProcessor(init=False),
            server_repository=MockServerRepository(),
            json_exporter=MockJsonExporter()
        )
        self.assertFalse(svc1.is_initialized())

        svc2 = Service(
            subprocessor=MockSubProcessor(),
            server_repository=MockServerRepository(init=False),
            json_exporter=MockJsonExporter()
        )
        self.assertFalse(svc2.is_initialized())

        svc3 = Service(
            subprocessor=MockSubProcessor(),
            server_repository=MockServerRepository(),
            json_exporter=MockJsonExporter(init=False)
        )
        self.assertFalse(svc3.is_initialized())

    def test_resolve_server_from_repo_matching_id(self) -> None:
        s1 = create_sample_server(1)
        s2 = create_sample_server(2)
        repo = MockServerRepository(servers=[s1, s2])
        svc = Service(
            subprocessor=MockSubProcessor(),
            server_repository=repo,
            json_exporter=MockJsonExporter()
        )
        res = svc._resolve_server(server_id=2)
        self.assertEqual(res, s2)

    def test_resolve_server_fallback_first(self) -> None:
        s1 = create_sample_server(1)
        repo = MockServerRepository(servers=[s1])
        svc = Service(
            subprocessor=MockSubProcessor(),
            server_repository=repo,
            json_exporter=MockJsonExporter()
        )
        res = svc._resolve_server(server_id=999)
        self.assertEqual(res, s1)

    def test_resolve_server_fetch_when_repo_empty(self) -> None:
        s1 = create_sample_server(1)
        sub = MockSubProcessor(return_data={'servers': [s1]})
        repo = MockServerRepository(servers=[])
        svc = Service(
            subprocessor=sub,
            server_repository=repo,
            json_exporter=MockJsonExporter()
        )
        res = svc._resolve_server()
        self.assertEqual(res, s1)

    def test_resolve_server_empty_fetch_returns_none(self) -> None:
        sub = MockSubProcessor(return_data={'servers': []})
        repo = MockServerRepository(servers=[])
        svc = Service(
            subprocessor=sub,
            server_repository=repo,
            json_exporter=MockJsonExporter()
        )
        res = svc._resolve_server()
        self.assertIsNone(res)

    def test_execute_speed_success(self) -> None:
        s1 = create_sample_server(1)
        sub = MockSubProcessor(return_data={'ping': 12.0, 'download': 120.0, 'upload': 45.0})
        repo = MockServerRepository(servers=[s1])
        svc = Service(subprocessor=sub, server_repository=repo, json_exporter=MockJsonExporter())

        result = svc.execute_speed(server_id=1)
        self.assertIsNotNone(result)
        self.assertEqual(result.download_speed, 120.0)
        self.assertEqual(result.upload_speed, 45.0)
        self.assertEqual(result.latency, 12.0)
        self.assertEqual(len(repo.saved_stats), 1)

    def test_execute_speed_none_server(self) -> None:
        sub = MockSubProcessor(return_data={'servers': []})
        repo = MockServerRepository(servers=[])
        svc = Service(subprocessor=sub, server_repository=repo, json_exporter=MockJsonExporter())
        self.assertIsNone(svc.execute_speed())

    def test_execute_download_success(self) -> None:
        s1 = create_sample_server(1)
        sub = MockSubProcessor(return_data={'download': 150.0})
        repo = MockServerRepository(servers=[s1])
        svc = Service(subprocessor=sub, server_repository=repo, json_exporter=MockJsonExporter())

        speed, srv = svc.execute_download(server_id=1)
        self.assertEqual(speed, 150.0)
        self.assertEqual(srv, s1)
        self.assertEqual(len(repo.saved_stats), 1)

    def test_execute_download_none_server(self) -> None:
        sub = MockSubProcessor(return_data={'servers': []})
        repo = MockServerRepository(servers=[])
        svc = Service(subprocessor=sub, server_repository=repo, json_exporter=MockJsonExporter())
        speed, srv = svc.execute_download()
        self.assertEqual(speed, 0.0)
        self.assertIsNone(srv)

    def test_execute_upload_success(self) -> None:
        s1 = create_sample_server(1)
        sub = MockSubProcessor(return_data={'upload': 50.0})
        repo = MockServerRepository(servers=[s1])
        svc = Service(subprocessor=sub, server_repository=repo, json_exporter=MockJsonExporter())

        speed, srv = svc.execute_upload(server_id=1)
        self.assertEqual(speed, 50.0)
        self.assertEqual(srv, s1)
        self.assertEqual(len(repo.saved_stats), 1)

    def test_execute_upload_none_server(self) -> None:
        sub = MockSubProcessor(return_data={'servers': []})
        repo = MockServerRepository(servers=[])
        svc = Service(subprocessor=sub, server_repository=repo, json_exporter=MockJsonExporter())
        speed, srv = svc.execute_upload()
        self.assertEqual(speed, 0.0)
        self.assertIsNone(srv)

    def test_fetch_servers_non_list(self) -> None:
        sub = MockSubProcessor(return_data={'servers': 'invalid'})
        repo = MockServerRepository(servers=[])
        svc = Service(subprocessor=sub, server_repository=repo, json_exporter=MockJsonExporter())
        res = svc.fetch_servers()
        self.assertEqual(res, [])

    def test_get_history_and_export_load_json(self) -> None:
        repo = MockServerRepository()
        exp = MockJsonExporter()
        svc = Service(subprocessor=MockSubProcessor(), server_repository=repo, json_exporter=exp)

        history = svc.get_history(limit=10)
        self.assertEqual(history, [])

        self.assertTrue(svc.export_json({'key': 'val'}, 'out.json'))
        self.assertEqual(len(exp.exported_data), 1)

        loaded = svc.load_json('in.json')
        self.assertEqual(loaded, {'loaded': 'in.json'})


if __name__ == '__main__':
    unittest.main()
