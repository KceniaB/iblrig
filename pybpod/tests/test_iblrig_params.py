import os
import shutil
from pathlib import Path

from pybpodgui_api.models.project import Project
from pybpodgui_plugin.__main__ import start as pybpod_start


def create_setup(exp, setup_name: str, board: str, subj: object, task: str = None):
    # task name is defined as the experiment_name + '_' + setup_name
    # Create or get preexisting setup
    setup = exp.create_setup()
    setup.name = setup_name
    setup.task = task if isinstance(task, str) else exp.name + "_" + setup_name
    setup.board = board
    setup += subj
    setup.detached = True
    return setup


def setup_iblpybpod_for_iblrig_params(iblrig_path: Path, iblrig_params_path: Path):
    # Set path vars
    iblrig_tasks_path = iblrig_path / "tasks"
    iblrig_params_plugins_path = iblrig_params_path / "plugins"
    iblrig_params_project_path = iblrig_params_path / "IBL"
    iblrig_params_project_tasks_path = iblrig_params_project_path / "tasks"

    # Create dirs if they do not already exist
    os.makedirs(iblrig_params_path, exist_ok=True)
    os.makedirs(Path(iblrig_params_plugins_path), exist_ok=True)

    # Copy pybpod user settings from iblrig repo to params dir
    src_file = iblrig_path / "scripts" / "user_settings.py"
    dst_file = iblrig_params_path / "user_settings.py"
    shutil.copy(src_file, dst_file)

    # instantiate a project
    # p = Project()

    # create ibl project
    p = Project()
    p.name = "IBL"
    p.save(str(iblrig_params_project_path))


    # create ibl Board
    p = Project()
    p.load(iblrig_params_project_path)
    p.create_board()
    b = p.create_board()
    b.name = "SELECT_BOARD_NAME_(e.g.[_iblrig_mainenlab_behavior_0])"
    b.serial_port = "COM#"
    p.save(str(iblrig_params_project_path))

    # create ibl subjects
    p = Project()
    p.load(iblrig_params_project_path)
    subject = p.create_subject()
    subject.name = "_iblrig_test_mouse"
    p.save(str(iblrig_params_project_path))
    p = Project()
    p.load(iblrig_params_project_path)
    subject = p.create_subject()
    subject.name = "_iblrig_calibration"
    p.save(str(iblrig_params_project_path))

    # create ibl users
    p = Project()
    p.load(iblrig_params_project_path)
    user = p.create_user()
    user.name = "_iblrig_test_user"
    p.save(str(iblrig_params_project_path))

    # create ibl tasks
    task_names = [
        "_iblrig_calibration_screen",
        "_iblrig_calibration_water",
        "_iblrig_calibration_input_listner",
        "_iblrig_calibration_frame2TTL",
        "_iblrig_misc_flush_water",
        "_iblrig_misc_bpod_ttl_test",
        "_iblrig_misc_frame2TTL_freq_test",
        "_iblrig_tasks_biasedChoiceWorld",
        "_iblrig_tasks_habituationChoiceWorld",
        "_iblrig_tasks_trainingChoiceWorld",
        "_iblrig_tasks_ephysChoiceWorld",
        "_iblrig_tasks_ephys_certification",
        "_iblrig_tasks_passiveChoiceWorld",
        "_iblrig_tasks_passiveChoiceWorldIndependent"
    ]
    for task_name in task_names:
        # create task
        p = Project()
        p.load(iblrig_params_project_path)
        task = p.create_task()
        task.name = task_name
        p.save(str(iblrig_params_project_path))
        # configure task
        p = Project()
        p.load(iblrig_params_project_path)
        task = p.find_task(task_name)
        task._commands = []
        p.save(str(iblrig_params_project_path))

    # create ibl experiments
    experiment_names = ["_iblrig_calibration", "_iblrig_misc", "_iblrig_tasks"]
    for exp_name in experiment_names:
        p = Project()
        p.load(iblrig_params_project_path)
        exp = p.create_experiment()
        exp.name = exp_name
        p.save(str(iblrig_params_project_path))

    # create ibl setups
    experiment_names = ["_iblrig_calibration", "_iblrig_misc", "_iblrig_tasks"]
    for exp_name in experiment_names:
        p = Project()
        p.load(iblrig_params_project_path)
        exp = [e for e in p.experiments if e.name == exp_name]
        calib_subj = [s for s in p.subjects if s.name == "_iblrig_calibration"][0]
        test_subj = [s for s in p.subjects if s.name == "_iblrig_test_mouse"][0]
        if not exp:
            raise KeyError(f"Experiment {exp} not found")
        else:
            exp = exp[0]
        if exp.name == "_iblrig_calibration":
            screen = create_setup(exp, "screen", p.boards[0].name, calib_subj)  # noqa
            water = create_setup(exp, "water", p.boards[0].name, calib_subj)  # noqa
            input_listner = create_setup(exp, "input_listner", p.boards[0].name, calib_subj)  # noqa
            frame2TTL = create_setup(exp, "frame2TTL", p.boards[0].name, calib_subj)  # noqa
        if exp.name == "_iblrig_misc":
            flush_water = create_setup(exp, "flush_water", p.boards[0].name, test_subj)  # noqa
            bpod_ttl_test = create_setup(exp, "bpod_ttl_test", p.boards[0].name, test_subj)  # noqa
            frame2TTL_freq_test = create_setup(  # noqa
                exp, "frame2TTL_freq_test", p.boards[0].name, test_subj
            )
        if exp.name == "_iblrig_tasks":
            biasedChoiceWorld = create_setup(exp, "biasedChoiceWorld", p.boards[0].name, None)  # noqa
            habituationChoiceWorld = create_setup(  # noqa
                exp, "habituationChoiceWorld", p.boards[0].name, None
            )
            trainingChoiceWorld = create_setup(  # noqa
                exp, "trainingChoiceWorld", p.boards[0].name, None
            )
            ephys_certification = create_setup(  # noqa
                exp, "ephys_certification", p.boards[0].name, None
            )
            ephysChoiceWorld = create_setup(  # noqa
                exp,
                "ephysChoiceWorld_testing",
                p.boards[0].name,
                test_subj,
                task="_iblrig_tasks_ephysChoiceWorld",
            )
            passiveChoiceWorld = create_setup(  # noqa
                exp,
                "passiveChoiceWorld_testing",
                p.boards[0].name,
                test_subj,
                task="_iblrig_tasks_passiveChoiceWorld",
            )
            passiveChoiceWorldIndependent = create_setup(  # noqa
                exp,
                "passiveChoiceWorldIndependent",
                p.boards[0].name,
                test_subj,
                task="_iblrig_tasks_passiveChoiceWorldIndependent",
            )
        p.save(str(iblrig_params_project_path))

    # copy ibl task files
    shutil.copytree(iblrig_tasks_path, iblrig_params_project_tasks_path, dirs_exist_ok=True)


if __name__ == "__main__":
    iblrig_path = Path.home() / "Documents" / "repos" / "iblrig"
    iblrig_params_path = Path.home() / "Documents" / "iblrig_params"
    setup_iblpybpod_for_iblrig_params(iblrig_path, iblrig_params_path)
    os.chdir(iblrig_params_path)
    pybpod_start()
