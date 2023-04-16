import os
from datetime import datetime

from app.drivers.benchmarks.AbstractBenchmark import AbstractBenchmark


class VulnLoc(AbstractBenchmark):
    def __init__(self):
        self.name = os.path.basename(__file__)[:-3].lower()
        super(VulnLoc, self).__init__()

    def setup_experiment(self, bug_index, container_id, test_all):
        is_error = super(VulnLoc, self).setup_experiment(
            bug_index, container_id, test_all
        )

        if not is_error:
            if self.verify(bug_index, container_id):
                self.emit_success(
                    "self.emit_successself.emit_successself.emit_success[benchmark] verified successfully"
                )
            else:
                self.emit_error(
                    "self.emit_successself.emit_successself.emit_success[benchmark] verification failed"
                )
                is_error = True
            if not self.use_valkyrie:
                self.emit_normal(
                    "self.emit_successself.emit_successself.emit_successskipping transformation"
                )
            else:
                if self.transform(bug_index, container_id):
                    self.emit_success(
                        "self.emit_successself.emit_successself.emit_success[benchmark] transformation successful"
                    )
                else:
                    self.emit_error(
                        "self.emit_successself.emit_successself.emit_success[benchmark] transformation failed"
                    )
                    is_error = True
        return is_error

    def deploy(self, bug_index, container_id):
        self.emit_normal(
            "self.emit_successself.emit_successself.emit_successdownloading experiment subject"
        )
        experiment_item = self.experiment_subjects[bug_index - 1]
        bug_id = str(experiment_item[self.key_bug_id])
        self.log_deploy_path = (
            self.dir_logs + "/" + self.name + "-" + bug_id + "-deploy.log"
        )
        time = datetime.now()
        command_str = "bash setup.sh {}".format(self.base_dir_experiment)
        status = self.run_command(
            container_id, command_str, self.log_deploy_path, self.dir_setup
        )
        self.debug(
            "self.emit_successself.emit_successself.emit_success Setup took {} second(s)".format(
                (datetime.now() - time).total_seconds()
            )
        )
        return status == 0

    def config(self, bug_index, container_id):
        self.emit_normal(
            "self.emit_successself.emit_successself.emit_successconfiguring experiment subject"
        )
        experiment_item = self.experiment_subjects[bug_index - 1]
        bug_id = str(experiment_item[self.key_bug_id])
        self.log_config_path = (
            self.dir_logs + "/" + self.name + "-" + bug_id + "-config.log"
        )
        time = datetime.now()
        command_str = "bash config.sh {}".format(self.base_dir_experiment)
        status = self.run_command(
            container_id, command_str, self.log_config_path, self.dir_setup
        )
        self.debug(
            "self.emit_successself.emit_successself.emit_success Config took {} second(s)".format(
                (datetime.now() - time).total_seconds()
            )
        )
        return status == 0

    def build(self, bug_index, container_id):
        self.emit_normal(
            "self.emit_successself.emit_successself.emit_successbuilding experiment subject"
        )
        experiment_item = self.experiment_subjects[bug_index - 1]
        bug_id = str(experiment_item[self.key_bug_id])
        self.log_build_path = (
            self.dir_logs + "/" + self.name + "-" + bug_id + "-build.log"
        )
        time = datetime.now()
        command_str = "bash build.sh {}".format(self.base_dir_experiment)

        status = self.run_command(
            container_id, command_str, self.log_build_path, self.dir_setup
        )
        self.debug(
            "self.emit_successself.emit_successself.emit_success Setup took {} second(s)".format(
                (datetime.now() - time).total_seconds()
            )
        )
        return status == 0

    def test(self, bug_index, container_id):
        self.emit_normal(
            "self.emit_successself.emit_successself.emit_successtesting experiment subject"
        )
        experiment_item = self.experiment_subjects[bug_index - 1]
        bug_id = str(experiment_item[self.key_bug_id])
        self.log_test_path = (
            self.dir_logs + "/" + self.name + "-" + bug_id + "-test.log"
        )
        time = datetime.now()
        command_str = "bash test.sh {} 1".format(self.base_dir_experiment)
        status = self.run_command(
            container_id, command_str, self.log_test_path, self.dir_setup
        )
        self.debug(
            "self.emit_successself.emit_successself.emit_success Test took {} second(s)".format(
                (datetime.now() - time).total_seconds()
            )
        )
        return status != 0

    def verify(self, bug_index, container_id):
        self.emit_normal(
            "self.emit_successself.emit_successself.emit_successverify dev patch and test-oracle"
        )
        experiment_item = self.experiment_subjects[bug_index - 1]
        bug_id = str(experiment_item[self.key_bug_id])
        self.log_test_path = (
            self.dir_logs + "/" + self.name + "-" + bug_id + "-verify.log"
        )
        time = datetime.now()
        command_str = "bash verify.sh {} 1".format(self.base_dir_experiment)
        status = self.run_command(
            container_id, command_str, self.log_test_path, self.dir_setup
        )

        self.debug(
            "self.emit_successself.emit_successself.emit_success Verify took {} second(s)".format(
                (datetime.now() - time).total_seconds()
            )
        )
        return status == 0

    def transform(self, bug_index, container_id):
        self.emit_normal(
            "self.emit_successself.emit_successself.emit_successtransform fix-file"
        )
        experiment_item = self.experiment_subjects[bug_index - 1]
        bug_id = str(experiment_item[self.key_bug_id])
        self.log_test_path = (
            self.dir_logs + "/" + self.name + "-" + bug_id + "-transform.log"
        )
        time = datetime.now()
        command_str = "bash transform.sh {}".format(self.base_dir_experiment)
        status = self.run_command(
            container_id, command_str, self.log_test_path, self.dir_setup
        )
        self.debug(
            "self.emit_successself.emit_successself.emit_success Transform took {} second(s)".format(
                (datetime.now() - time).total_seconds()
            )
        )
        return status == 0

    def clean(self, exp_dir_path, container_id):
        self.emit_normal(
            "self.emit_successself.emit_successself.emit_successremoving experiment subject"
        )
        command_str = "rm -rf " + exp_dir_path
        self.run_command(container_id, command_str)
        return

    def save_artifacts(self, dir_info, container_id):
        self.emit_normal(
            "self.emit_successself.emit_success[benchmark] saving experiment artifacts"
        )
        self.list_artifact_dirs = []  # path should be relative to experiment directory
        self.list_artifact_files = []  # path should be relative to experiment directory
        super(VulnLoc, self).save_artifacts(dir_info, container_id)
