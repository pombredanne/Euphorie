import unittest
from zope.interface import Interface
from zope.schema import Choice
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm
from euphorie.deployment.tests.functional import EuphorieFunctionalTestCase


class context_menu_tests(unittest.TestCase):
    def context_menu(self, *a, **kw):
        from euphorie.client.api import context_menu
        return context_menu(*a, **kw)

    def test_empty_menu(self):
        import mock
        with mock.patch('euphorie.client.api.getTreeData',
                return_value={'children': []}):
            self.assertEqual(
                    self.context_menu(mock.Mock(), 'context', 'phase', None),
                    [])

    def test_risk_status_no_class_set(self):
        import mock
        menu = {'children': [{
                        'id': 15,
                        'type': 'risk',
                        'class': None,
                        'leaf_module': True,
                        'path': '/1',
                        'current_parent': False,
                        'url': '/1',
                        'children': [],
                        }]}
        request = mock.Mock()
        request.survey_session.absolute_url.return_value = 'http://localhost'
        with mock.patch('euphorie.client.api.getTreeData', return_value=menu):
            context_menu = self.context_menu(request, 'context', 'phase', None)
            self.assertEqual(context_menu[0]['status'], None)

    def test_risk_status_postponed(self):
        import mock
        menu = {'children': [{
                        'id': 15,
                        'type': 'risk',
                        'class': 'postponed',
                        'leaf_module': True,
                        'path': '/1',
                        'current_parent': False,
                        'url': '/1',
                        'children': [],
                        }]}
        request = mock.Mock()
        request.survey_session.absolute_url.return_value = 'http://localhost'
        with mock.patch('euphorie.client.api.getTreeData', return_value=menu):
            context_menu = self.context_menu(request, 'context', 'phase', None)
            self.assertEqual(context_menu[0]['status'], 'postponed')

    def test_risk_status_risk_present(self):
        import mock
        menu = {'children': [{
                        'id': 15,
                        'type': 'risk',
                        'class': 'answered risk',
                        'leaf_module': True,
                        'path': '/1',
                        'current_parent': False,
                        'url': '/1',
                        'children': [],
                        }]}
        request = mock.Mock()
        request.survey_session.absolute_url.return_value = 'http://localhost'
        with mock.patch('euphorie.client.api.getTreeData', return_value=menu):
            context_menu = self.context_menu(request, 'context', 'phase', None)
            self.assertEqual(context_menu[0]['status'], 'present')

    def test_risk_status_risk_not_present(self):
        import mock
        menu = {'children': [{
                        'id': 15,
                        'type': 'risk',
                        'class': 'current answered',
                        'leaf_module': True,
                        'path': '/1',
                        'current_parent': False,
                        'url': '/1',
                        'children': [],
                        }]}
        request = mock.Mock()
        request.survey_session.absolute_url.return_value = 'http://localhost'
        with mock.patch('euphorie.client.api.getTreeData', return_value=menu):
            context_menu = self.context_menu(request, 'context', 'phase', None)
            self.assertEqual(context_menu[0]['status'], 'not-present')

    def test_risk_status_risk_seen(self):
        import mock
        menu = {'children': [{
                        'id': 15,
                        'type': 'risk',
                        'class': 'current',
                        'leaf_module': True,
                        'path': '/1',
                        'current_parent': False,
                        'url': '/1',
                        'children': [],
                        }]}
        request = mock.Mock()
        request.survey_session.absolute_url.return_value = 'http://localhost'
        with mock.patch('euphorie.client.api.getTreeData', return_value=menu):
            context_menu = self.context_menu(request, 'context', 'phase', None)
            self.assertEqual(context_menu[0]['status'], None)


class get_json_token_tests(unittest.TestCase):
    def get_json_token(self, *a, **kw):
        from euphorie.client.api import get_json_token
        return get_json_token(*a, **kw)

    def test_missing_required_field(self):
        self.assertRaises(KeyError,
                self.get_json_token, {}, 'field', None, required=True)

    def test_missing_optional_field(self):
        self.assertEqual(
                self.get_json_token({}, 'field', None, required=False,
                    default='default'),
                'default')

    def test_bad_value(self):
        self.assertRaises(ValueError,
                self.get_json_token, {'field': 'oops'}, 'field',
                DummySchema['field'])

    def test_correct_value(self):
        self.assertEqual(
                self.get_json_token({'field': u'foo'}, 'field',
                    DummySchema['field']),
                u'foo')


class get_json_string_tests(unittest.TestCase):
    def get_json_string(self, *a, **kw):
        from euphorie.client.api import get_json_string
        return get_json_string(*a, **kw)

    def test_missing_required_field(self):
        self.assertRaises(KeyError,
                self.get_json_string, {}, 'field', required=True)

    def test_missing_optional_field(self):
        self.assertEqual(
                self.get_json_string({}, 'field', required=False,
                    default='default'),
                'default')

    def test_bad_type(self):
        self.assertRaises(ValueError,
                self.get_json_string, {'field': False}, 'field',
                DummySchema['field'])

    def test_proper_value(self):
        self.assertEqual(
                self.get_json_string({'field': 'value'}, 'field'),
                'value')

    def test_trim_length(self):
        self.assertEqual(
                self.get_json_string({'field': 'value'}, 'field', length=2),
                'va')


class get_json_bool_tests(unittest.TestCase):
    def get_json_bool(self, *a, **kw):
        from euphorie.client.api import get_json_bool
        return get_json_bool(*a, **kw)

    def test_missing_required_field(self):
        self.assertRaises(KeyError,
                self.get_json_bool, {}, 'field', required=True)

    def test_missing_optional_field(self):
        self.assertEqual(
                self.get_json_bool({}, 'field', required=False,
                    default='default'),
                'default')

    def test_bad_type(self):
        self.assertRaises(ValueError,
                self.get_json_bool, {'field': 'dummy'}, 'field',
                DummySchema['field'])

    def test_proper_value(self):
        self.assertEqual(self.get_json_bool({'field': True}, 'field'), True)


class get_json_int_tests(unittest.TestCase):
    def get_json_int(self, *a, **kw):
        from euphorie.client.api import get_json_int
        return get_json_int(*a, **kw)

    def test_missing_required_field(self):
        self.assertRaises(KeyError,
                self.get_json_int, {}, 'field', required=True)

    def test_missing_optional_field(self):
        self.assertEqual(
                self.get_json_int({}, 'field', required=False,
                    default='default'),
                'default')

    def test_bad_type(self):
        self.assertRaises(ValueError,
                self.get_json_int, {'field': 'dummy'}, 'field',
                DummySchema['field'])

    def test_proper_value(self):
        self.assertEqual(self.get_json_int({'field': 15}, 'field'), 15)


class get_json_date_tests(unittest.TestCase):
    def get_json_date(self, *a, **kw):
        from euphorie.client.api import get_json_date
        return get_json_date(*a, **kw)

    def test_missing_required_field(self):
        self.assertRaises(KeyError,
                self.get_json_date, {}, 'field', required=True)

    def test_missing_optional_field(self):
        self.assertEqual(
                self.get_json_date({}, 'field', required=False,
                    default='default'),
                'default')

    def test_bad_type(self):
        self.assertRaises(ValueError,
                self.get_json_date, {'field': 15}, 'field',
                DummySchema['field'])

    def test_invalid_date(self):
        self.assertRaises(ValueError,
                self.get_json_date, {'field': '2012-06-four'}, 'field',
                DummySchema['field'])

    def test_proper_value(self):
        import datetime
        self.assertEqual(
                self.get_json_date({'field': '2012-06-04'}, 'field'),
                datetime.date(2012, 6, 4))


class export_image_tests(EuphorieFunctionalTestCase):
    def export_image(self, *a, **kw):
        from .. import export_image
        return export_image(*a, **kw)

    def setup_context(self):
        from plone.namedfile.file import NamedBlobImage
        self.loginAsPortalOwner()
        self.portal.sectors.nl.invokeFactory('euphorie.sector', 'dining',
                title=u'Fine dining')
        sector = self.portal.sectors.nl.dining
        sector.invokeFactory('euphorie.surveygroup', 'survey', title=u'Survey')
        surveygroup = sector.survey
        surveygroup.invokeFactory('euphorie.survey', 'version1',
                title=u'Version 1')
        survey = surveygroup.version1
        survey.invokeFactory('euphorie.module', '1', title=u'Module 1')
        module = survey['1']
        gif = 'GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff' \
               '\xff\xff!\xf9\x04\x01\x00\x00\x01\x00,\x00\x00\x00' \
               '\x00\x01\x00\x01\x00\x00\x02\x01L\x00;'
        module.image = NamedBlobImage(data=gif, contentType='image/gif',
                filename=u'pixel.gif')
        module.caption = u'Caption'
        view = survey.restrictedTraverse('@@publish')
        view.publish()
        return self.portal.client['nl']['dining']['survey']['1']

    def test_unknown_image(self):
        from zope.publisher.browser import TestRequest
        context = self.setup_context()
        context.image = None
        request = TestRequest()
        response = self.export_image(context, request, 'image', u'Caption',
                width=100, height=100)
        self.assertEqual(response, None)

    def test_standard(self):
        from zope.component import getUtility
        from z3c.appconfig.interfaces import IAppConfig
        from zope.publisher.browser import TestRequest
        config = getUtility(IAppConfig)
        del config['euphorie']['client']
        context = self.setup_context()
        request = TestRequest()
        request.client = self.portal.client
        response = self.export_image(context, request, 'image', 'caption',
                width=100, height=100)
        self.assertEqual(
                set(response), set(['thumbnail', 'original', 'caption']))
        self.assertTrue(response['thumbnail']
                .startswith('http://nohost/plone/client/nl'))
        self.assertTrue(response['original']
                .startswith('http://nohost/plone/client/nl'))
        self.assertEqual(response['caption'], u'Caption')

    def test_different_client_url(self):
        from zope.component import getUtility
        from z3c.appconfig.interfaces import IAppConfig
        from zope.publisher.browser import TestRequest
        config = getUtility(IAppConfig)
        config['euphorie']['client'] = 'http://client.euphorie.org/'
        context = self.setup_context()
        request = TestRequest()
        request.client = self.portal.client
        response = self.export_image(context, request, 'image', 'caption',
                width=100, height=100)
        self.assertTrue(response['thumbnail']
                .startswith('http://client.euphorie.org/nl/'))
        self.assertTrue(response['original']
                .startswith('http://client.euphorie.org/nl/'))


class JsonViewTests(unittest.TestCase):
    def JsonView(self, *a, **kw):
        from .. import JsonView
        return JsonView(*a, **kw)

    def test_invalid_input(self):
        import json
        import StringIO
        from zope.publisher.browser import TestRequest
        request = TestRequest()
        request.stdin = StringIO.StringIO('invalid json')
        view = self.JsonView(None, request)
        response = view()
        self.assertEqual(
                json.loads(response),
                {'type': 'error',
                 'message': 'Invalid JSON input'})

    def test_bad_method(self):
        import json
        import StringIO
        import mock
        from zope.publisher.browser import TestRequest
        request = TestRequest()
        request.stdin = StringIO.StringIO()
        context = mock.Mock()
        context.getPhysicalPath.return_value = ['', 'Plone', 'client', 'api']
        view = self.JsonView(context, request)
        response = view()
        self.assertEqual(request.response.getStatus(), 405)
        self.assertEqual(
                json.loads(response),
                {'type': 'error',
                 'message': 'HTTP method not allowed'})


class DummySchema(Interface):
    field = Choice(vocabulary=SimpleVocabulary([
        SimpleTerm(u'foo', title=u'Bar')]))
