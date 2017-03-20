# -*- coding: utf-8 -*-

from httplib import OK, NOT_FOUND
from unittest import TestCase
import json
import pkg_resources

from openfisca_web_api.app import create_app

TEST_COUNTRY_PACKAGE = 'openfisca_dummy_country'
distribution = pkg_resources.get_distribution(TEST_COUNTRY_PACKAGE)
subject = create_app(TEST_COUNTRY_PACKAGE).test_client()


class ParametersRoute(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.response = subject.get('/parameters')

    def test_return_code(self):
        self.assertEqual(self.response.status_code, OK)

    def test_package_name_header(self):
        self.assertEqual(self.response.headers.get('Country-Package'), distribution.key)

    def test_package_version_header(self):
        self.assertEqual(self.response.headers.get('Country-Package-Version'), distribution.version)

    def test_response_data(self):
        parameters = json.loads(self.response.data)
        self.assertEqual(
            parameters[u'impot.taux'],
            {u'description': u'taux d\'impôt sur les salaires'}
            )


class ParameterRoute(TestCase):

    def test_error_code_non_existing_parameter(self):
        response = subject.get('/parameter/non.existing.parameter')
        self.assertEqual(response.status_code, NOT_FOUND)

    def test_return_code_existing_parameter(self):
        response = subject.get('/parameter/impot.taux')
        self.assertEqual(response.status_code, OK)

    def test_fuzzied_parameter_values(self):
        response = subject.get('/parameter/impot.taux')
        parameter = json.loads(response.data)
        self.assertEqual(
            parameter,
            {
                u'id': u'impot.taux',
                u'description': u'taux d\'impôt sur les salaires',
                u'values': {u'2016-01-01': 0.35, u'2015-01-01': 0.32, u'1998-01-01': 0.3}
                }
            )

    def test_stopped_parameter_values(self):
        response = subject.get('/parameter/csg.activite.deductible.taux')
        parameter = json.loads(response.data)
        self.assertEqual(
            parameter,
            {
                u'id': u'csg.activite.deductible.taux',
                u'description': u'taux de la CSG déductible',
                u'values': {u'2016-01-01': None, u'2015-01-01': 0.06, u'1998-01-01': 0.051}
                }
            )
