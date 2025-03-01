import os
from os.path import join
from typing import List

from app.drivers.benchmarks.AbstractBenchmark import AbstractBenchmark


class Bears(AbstractBenchmark):

    log_instrument_path = None

    def __init__(self):
        self.name = os.path.basename(__file__)[:-3].lower()
        super(Bears, self).__init__()

    def setup_experiment(self, bug_index, container_id, test_all):
        is_error = super(Bears, self).setup_experiment(
            bug_index, container_id, test_all
        )
        if not is_error:
            if self.instrument(bug_index, container_id):
                self.emit_success("[benchmark] instrumentation successful")
            else:
                self.emit_error("[benchmark] instrumentation failed")
                is_error = True
        return is_error

    def setup_container(self, bug_index, image_name, cpu: List[str], gpu: List[str]):
        """
        Setup the container for the experiment by constructing volumes,
        which point to certain folders in the project
        """
        container_id = super(Bears, self).setup_container(
            bug_index, image_name, cpu, gpu
        )

        experiment_item = self.experiment_subjects[bug_index - 1]
        bug_id = str(experiment_item[self.key_bug_id])

        self.run_command(
            container_id,
            "git clone https://github.com/bears-bugs/bears-benchmark {}".format(
                join(self.dir_expr, "src")
            ),
        )

        self.run_command(
            container_id,
            "git checkout {}".format(bug_id),
            dir_path=join(self.dir_expr, "src"),
        )

        self.run_command(
            container_id, "git checkout HEAD~2", dir_path=join(self.dir_expr, "src")
        )

        return container_id

    def deploy(self, bug_index, container_id):
        self.emit_normal("downloading experiment subject")
        return True

    def config(self, bug_index, container_id):
        self.emit_normal("configuring experiment subject")
        return True

    def build(self, bug_index, container_id):
        self.emit_normal("building experiment subject")
        status = self.run_command(
            container_id, "mvn compile -DskipTests", dir_path=join(self.dir_expr, "src")
        )
        return status == 0

    def test(self, bug_index, container_id):
        self.emit_normal("testing experiment subject")
        status = self.run_command(
            container_id, "mvn test", dir_path=join(self.dir_expr, "src")
        )
        return status != 0

    def instrument(self, bug_index, container_id):
        self.emit_normal("instrumenting assertions")
        return True

    def clean(self, exp_dir_path, container_id):
        self.emit_normal("removing experiment subject")
        command_str = "rm -rf " + exp_dir_path
        self.run_command(container_id, command_str)
        return

    def save_artifacts(self, dir_info, container_id):
        self.list_artifact_dirs = []  # path should be relative to experiment directory
        self.list_artifact_files = []  # path should be relative to experiment directory
        super(Bears, self).save_artifacts(dir_info, container_id)
