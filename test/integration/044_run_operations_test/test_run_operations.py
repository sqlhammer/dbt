from test.integration.base import DBTIntegrationTest, use_profile
import yaml


class TestOperations(DBTIntegrationTest):
    @property
    def schema(self):
        return "run_operations_044"

    @property
    def models(self):
        return "test/integration/044_run_operations_test/models"

    @property
    def project_config(self):
        return {
            "macro-paths": ['test/integration/044_run_operations_test/macros'],
        }

    def run_operation(self, macro, expect_pass=True, extra_args=None, **kwargs):
        args = ['run-operation']
        if macro:
            args.extend(('--macro', macro))
        if kwargs:
            args.extend(('--args', yaml.safe_dump(kwargs)))
        if extra_args:
            args.extend(extra_args)
        return self.run_dbt(args, expect_pass=expect_pass)

    @use_profile('postgres')
    def test__postgres_macro_noargs(self):
        self.run_operation('no_args')
        self.assertTableDoesExist('no_args')

    @use_profile('postgres')
    def test__postgres_macro_args(self):
        self.run_operation('table_name_args', table_name='my_fancy_table')
        self.assertTableDoesExist('my_fancy_table')

    @use_profile('postgres')
    def test__postgres_macro_exception(self):
        self.run_operation('syntax_error', False)

    @use_profile('postgres')
    def test__postgres_macro_missing(self):
        self.run_operation('this_macro_does_not_exist', False)

    @use_profile('postgres')
    def test__postgres_cannot_connect(self):
        self.run_operation('no_args',
                           extra_args=['--target', 'noaccess'],
                           expect_pass=False)
