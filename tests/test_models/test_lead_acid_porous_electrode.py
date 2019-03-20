#
# Tests for the lead-acid composite model
#
from __future__ import absolute_import, division
from __future__ import print_function, unicode_literals
import pybamm
import tests

import unittest
import numpy as np


class TestLeadAcidPorousElectrode(unittest.TestCase):
    def test_basic_processing(self):
        model = pybamm.lead_acid.PorousElectrode()

        modeltest = tests.StandardModelTest(model)
        modeltest.test_all()

    def test_solution(self):
        model = pybamm.lead_acid.PorousElectrode()
        modeltest = tests.StandardModelTest(model)
        modeltest.test_all()
        T, Y = modeltest.solver.t, modeltest.solver.y

        # check output
        for idx in range(len(T) - 1):
            # Check concentration decreases
            np.testing.assert_array_less(
                model.variables["Electrolyte concentration"].evaluate(
                    T[idx + 1], Y[:, idx + 1]
                ),
                model.variables["Electrolyte concentration"].evaluate(
                    T[idx], Y[:, idx]
                ),
            )
            # Check cut-off
            np.testing.assert_array_less(
                0,
                model.variables["Electrolyte concentration"].evaluate(
                    T[idx + 1], Y[:, idx + 1]
                ),
            )
            self.assertLess(
                model.variables["Voltage"].evaluate(T[idx + 1], Y[:, idx + 1]),
                model.variables["Voltage"].evaluate(T[idx], Y[:, idx]),
            )


if __name__ == "__main__":
    print("Add -v for more debug output")
    import sys

    if "-v" in sys.argv:
        debug = True
    unittest.main()
