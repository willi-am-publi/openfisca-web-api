# -*- coding: utf-8 -*-


# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013, 2014, 2015 OpenFisca Team
# https://github.com/openfisca
#
# This file is part of OpenFisca.
#
# OpenFisca is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# OpenFisca is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


"""Fields controller"""


import collections
import datetime

from openfisca_core import periods, simulations

from .. import contexts, environment, model, wsgihelpers


@wsgihelpers.wsgify
def api1_variables(req):
    ctx = contexts.Ctx(req)
    headers = wsgihelpers.handle_cross_origin_resource_sharing(ctx)

    assert req.method == 'GET', req.method

    simulation = None
    variables_json = []
    for variable_name, column in model.tax_benefit_system.column_by_name.iteritems():
        variable_json = column.to_json()
        if column.is_formula():
            if simulation is None:
                simulation = simulations.Simulation(
                    period = periods.period(datetime.date.today().year),
                    tax_benefit_system = model.tax_benefit_system,
                    )
            holder = simulation.get_or_new_holder(variable_name)
            variable_json['formula'] = holder.formula.to_json(
                get_input_variables_and_parameters = model.get_cached_input_variables_and_parameters,
                )
        variables_json.append(variable_json)

    return wsgihelpers.respond_json(ctx,
        collections.OrderedDict(sorted(dict(
            apiVersion = 1,
            country_package_git_head_sha = environment.country_package_git_head_sha,
            method = req.script_name,
            url = req.url.decode('utf-8'),
            variables = variables_json,
            ).iteritems())),
        headers = headers,
        )
