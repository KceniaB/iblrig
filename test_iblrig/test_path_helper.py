import tempfile
import unittest
from pathlib import Path

from iblrig import path_helper
# import iblrig.path_helper as ph


class TestPathHelper(unittest.TestCase):
    def setUp(self):
        pass

    def test_get_iblserver_data_path(self):
        df = path_helper.get_iblserver_data_path(subjects=True)
        self.assertTrue(isinstance(df, Path))
        self.assertTrue("Subjects" in str(df))
        df = path_helper.get_iblserver_data_path(subjects=False)
        self.assertTrue(isinstance(df, Path))
        self.assertTrue("Subjects" not in str(df))

    def test_get_iblrig_path(self):
        f = path_helper.get_iblrig_path()
        self.assertTrue(isinstance(f, Path))
        self.assertTrue("iblrig" in str(f))

    def test_get_iblrig_params_path(self):
        f = path_helper.get_iblrig_params_path()
        self.assertTrue(isinstance(f, Path))
        self.assertTrue("iblrig_params" in str(f))

    def test_get_iblrig_local_data_path(self):
        df = path_helper.get_iblrig_local_data_path(subjects=False)
        self.assertTrue(isinstance(df, Path))
        self.assertTrue("iblrig_data" in str(df))
        self.assertTrue("Subjects" not in str(df))
        dfs = path_helper.get_iblrig_local_data_path(subjects=True)
        self.assertTrue(isinstance(dfs, Path))
        self.assertTrue("iblrig_data" in str(dfs))
        self.assertTrue("Subjects" in str(dfs))

    def test_get_previous_session_folders(self):
        test_subject_name = "_iblrig_test_mouse"
        self.local_dir = tempfile.TemporaryDirectory()
        self.remote_dir = tempfile.TemporaryDirectory()

        def create_local_session() -> str:
            local_session_path = Path(self.local_dir.name) / "Subjects" / test_subject_name / "1970-01-01" / "001"
            local_session_path.mkdir(parents=True)
            return str(local_session_path)

        def create_remote_subject() -> str:
            remote_subject_dir = Path(self.remote_dir.name) / "Subjects"
            remote_subject_dir.mkdir(parents=True)
            return str(remote_subject_dir)

        def assert_values(previous_session_folders):
            self.assertTrue(isinstance(previous_session_folders, list))
            if previous_session_folders:
                # returned list is not empty and should contain strings
                for session_folder in previous_session_folders:
                    self.assertTrue(isinstance(session_folder, str))

        # Test for an existing subject, local does exist and remote does exist
        # Create local session and remote subject temp directories
        test_local_session_folder = create_local_session()
        test_remote_subject_folder = create_remote_subject()

        # Call the function
        test_previous_session_folders = path_helper.get_previous_session_folders(
            test_subject_name,
            test_local_session_folder,
            remote_subject_folder=test_remote_subject_folder,
        )
        assert_values(test_previous_session_folders)

        # Test for an existing subject, local does exist and remote does NOT exist
        self.remote_dir.cleanup()
        # Call the function
        test_previous_session_folders = path_helper.get_previous_session_folders(
            test_subject_name,
            test_local_session_folder,
            remote_subject_folder=test_remote_subject_folder,
        )
        assert_values(test_previous_session_folders)

        # Test for an existing subject, local does NOT exist and remote does exist
        self.local_dir.cleanup()
        test_remote_subject_folder = create_remote_subject()
        # Call the function
        test_previous_session_folders = path_helper.get_previous_session_folders(
            test_subject_name,
            test_local_session_folder,
            remote_subject_folder=test_remote_subject_folder,
        )
        assert_values(test_previous_session_folders)

        # Test for an existing subject, local does NOT exist and remote does NOT exist
        self.local_dir.cleanup()
        self.remote_dir.cleanup()
        # Call the function
        test_previous_session_folders = path_helper.get_previous_session_folders(
            test_subject_name,
            test_local_session_folder,
            remote_subject_folder=test_remote_subject_folder,
        )
        assert_values(test_previous_session_folders)

        # Test for a new subject
        test_new_subject_name = "_new_iblrig_test_mouse"
        test_new_session_folder = (Path(self.local_dir.name) / "Subjects" / test_new_subject_name / "1970-01-01" / "001")
        test_previous_session_folders = path_helper.get_previous_session_folders(test_new_subject_name, str(test_new_session_folder))
        self.assertTrue(isinstance(test_previous_session_folders, list))
        self.assertTrue(not test_previous_session_folders)  # returned list should be empty

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main(exit=False)
