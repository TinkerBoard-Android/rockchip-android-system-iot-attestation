"""Unit test for atft manager."""
import unittest

import atftman
import fastboot_exceptions

from mock import MagicMock
from mock import patch

files = []

class AtftManTest(unittest.TestCase):
  ATFA_TEST_SERIAL = 'ATFA_TEST_SERIAL'
  TEST_TMP_FOLDER = '/tmp/TMPTEST/'
  TEST_SERIAL = 'TEST_SERIAL'
  TEST_SERIAL2 = 'TEST_SERIAL2'
  TEST_SERIAL3 = 'TEST_SERIAL3'
  TEST_UUID = 'TEST-UUID'
  TEST_LOCATION = 'BUS1-PORT1'
  TEST_LOCATION2 = 'BUS2-PORT1'
  TEST_LOCATION3 = 'BUS1-PORT2'

  class FastbootDeviceTemplate(object):

    @staticmethod
    def ListDevices():
      pass

    def __init__(self, serial_number):
      self.serial_number = serial_number

    def Oem(self, oem_command, err_to_out):
      pass

    def Upload(self, file_path):
      pass

    def GetVar(self, var):
      pass

    def Download(self, file_path):
      pass

    def Disconnect(self):
      pass

    def __del__(self):
      pass

  def MockInit(self, serial_number):
    mock_instance = MagicMock()
    mock_instance.serial_number = serial_number
    return mock_instance

  def setUp(self):
    self.mock_serial_mapper = MagicMock()
    self.mock_serial_instance = MagicMock()
    self.mock_serial_mapper.return_value = self.mock_serial_instance
    self.mock_serial_instance.get_serial_map.return_value = []

  # Test AtftManager.ListDevices
  @patch('__main__.AtftManTest.FastbootDeviceTemplate.ListDevices')
  def testListDevicesNormal(self, mock_list_devices):
    atft_manager = atftman.AtftManager(self.FastbootDeviceTemplate,
                                       self.mock_serial_mapper)
    mock_list_devices.return_value = [self.TEST_SERIAL,
                                      self.ATFA_TEST_SERIAL]
    atft_manager.ListDevices()
    atft_manager.ListDevices()
    self.assertEqual(atft_manager.atfa_dev.serial_number,
                     self.ATFA_TEST_SERIAL)
    self.assertEqual(1, len(atft_manager.target_devs))
    self.assertEqual(atft_manager.target_devs[0].serial_number,
                     self.TEST_SERIAL)

  @patch('__main__.AtftManTest.FastbootDeviceTemplate.ListDevices')
  def testListDevicesATFA(self, mock_list_devices):
    atft_manager = atftman.AtftManager(self.FastbootDeviceTemplate,
                                       self.mock_serial_mapper)
    mock_list_devices.return_value = [self.ATFA_TEST_SERIAL]
    atft_manager.ListDevices()
    atft_manager.ListDevices()
    self.assertEqual(atft_manager.atfa_dev.serial_number,
                     self.ATFA_TEST_SERIAL)
    self.assertEqual(0, len(atft_manager.target_devs))

  @patch('__main__.AtftManTest.FastbootDeviceTemplate.ListDevices')
  def testListDevicesTarget(self, mock_list_devices):
    atft_manager = atftman.AtftManager(self.FastbootDeviceTemplate,
                                       self.mock_serial_mapper)
    mock_list_devices.return_value = [self.TEST_SERIAL]
    atft_manager.ListDevices()
    atft_manager.ListDevices()
    self.assertEqual(atft_manager.atfa_dev, None)
    self.assertEqual(1, len(atft_manager.target_devs))
    self.assertEqual(atft_manager.target_devs[0].serial_number,
                     self.TEST_SERIAL)

  @patch('__main__.AtftManTest.FastbootDeviceTemplate.ListDevices')
  def testListDevicesMultipleTargets(self, mock_list_devices):
    atft_manager = atftman.AtftManager(self.FastbootDeviceTemplate,
                                       self.mock_serial_mapper)
    mock_list_devices.return_value = [self.TEST_SERIAL, self.TEST_SERIAL2]
    atft_manager.ListDevices()
    atft_manager.ListDevices()
    self.assertEqual(atft_manager.atfa_dev, None)
    self.assertEqual(2, len(atft_manager.target_devs))
    self.assertEqual(atft_manager.target_devs[0].serial_number,
                     self.TEST_SERIAL)
    self.assertEqual(atft_manager.target_devs[1].serial_number,
                     self.TEST_SERIAL2)


  def testListDevicesChangeNorm(self):
    mock_fastboot = MagicMock()
    mock_fastboot.side_effect = self.MockInit
    atft_manager = atftman.AtftManager(mock_fastboot,
                                       self.mock_serial_mapper)
    mock_fastboot.ListDevices.return_value = [self.ATFA_TEST_SERIAL]
    atft_manager.ListDevices()
    atft_manager.ListDevices()
    mock_fastboot.ListDevices.return_value = [self.TEST_SERIAL]
    atft_manager.ListDevices()
    atft_manager.ListDevices()
    self.assertEqual(atft_manager.atfa_dev, None)
    self.assertEqual(1, len(atft_manager.target_devs))
    self.assertEqual(atft_manager.target_devs[0].serial_number,
                     self.TEST_SERIAL)
    self.assertEqual(2, mock_fastboot.call_count)

  def testListDevicesChangeAdd(self):
    mock_fastboot = MagicMock()
    mock_fastboot.side_effect = self.MockInit
    atft_manager = atftman.AtftManager(mock_fastboot,
                                       self.mock_serial_mapper)
    mock_fastboot.ListDevices.return_value = [self.ATFA_TEST_SERIAL]
    atft_manager.ListDevices()
    atft_manager.ListDevices()
    mock_fastboot.ListDevices.return_value = [self.ATFA_TEST_SERIAL,
                                              self.TEST_SERIAL]
    atft_manager.ListDevices()
    atft_manager.ListDevices()
    self.assertEqual(atft_manager.atfa_dev.serial_number,
                     self.ATFA_TEST_SERIAL)
    self.assertEqual(1, len(atft_manager.target_devs))
    self.assertEqual(atft_manager.target_devs[0].serial_number,
                     self.TEST_SERIAL)
    self.assertEqual(2, mock_fastboot.call_count)

  def testListDevicesChangeAddATFA(self):
    mock_fastboot = MagicMock()
    mock_fastboot.side_effect = self.MockInit
    atft_manager = atftman.AtftManager(mock_fastboot,
                                       self.mock_serial_mapper)
    mock_fastboot.ListDevices.return_value = [self.TEST_SERIAL]
    atft_manager.ListDevices()
    atft_manager.ListDevices()
    mock_fastboot.ListDevices.return_value = [self.ATFA_TEST_SERIAL,
                                              self.TEST_SERIAL]
    atft_manager.ListDevices()
    atft_manager.ListDevices()
    self.assertEqual(atft_manager.atfa_dev.serial_number,
                     self.ATFA_TEST_SERIAL)
    self.assertEqual(1, len(atft_manager.target_devs))
    self.assertEqual(atft_manager.target_devs[0].serial_number,
                     self.TEST_SERIAL)
    self.assertEqual(2, mock_fastboot.call_count)

  def testListDevicesChangeCommon(self):
    mock_fastboot = MagicMock()
    mock_fastboot.side_effect = self.MockInit
    atft_manager = atftman.AtftManager(mock_fastboot,
                                       self.mock_serial_mapper)
    mock_fastboot.ListDevices.return_value = [self.ATFA_TEST_SERIAL,
                                              self.TEST_SERIAL]
    atft_manager.ListDevices()
    atft_manager.ListDevices()
    mock_fastboot.ListDevices.return_value = [self.TEST_SERIAL2,
                                              self.TEST_SERIAL]
    atft_manager.ListDevices()
    atft_manager.ListDevices()
    self.assertEqual(atft_manager.atfa_dev,
                     None)
    self.assertEqual(2, len(atft_manager.target_devs))
    self.assertEqual(atft_manager.target_devs[0].serial_number,
                     self.TEST_SERIAL)
    self.assertEqual(atft_manager.target_devs[1].serial_number,
                     self.TEST_SERIAL2)
    self.assertEqual(3, mock_fastboot.call_count)

  def testListDevicesChangeCommonATFA(self):
    mock_fastboot = MagicMock()
    mock_fastboot.side_effect = self.MockInit
    atft_manager = atftman.AtftManager(mock_fastboot,
                                       self.mock_serial_mapper)
    mock_fastboot.ListDevices.return_value = [self.ATFA_TEST_SERIAL,
                                              self.TEST_SERIAL]
    atft_manager.ListDevices()
    atft_manager.ListDevices()
    mock_fastboot.ListDevices.return_value = [self.ATFA_TEST_SERIAL,
                                              self.TEST_SERIAL2]
    atft_manager.ListDevices()
    # First refresh, TEST_SERIAL should disappear
    self.assertEqual(0, len(atft_manager.target_devs))
    # Second refresh, TEST_SERIAL2 should be added
    atft_manager.ListDevices()
    self.assertEqual(atft_manager.atfa_dev.serial_number,
                     self.ATFA_TEST_SERIAL)
    self.assertEqual(1, len(atft_manager.target_devs))
    self.assertEqual(atft_manager.target_devs[0].serial_number,
                     self.TEST_SERIAL2)
    self.assertEqual(3, mock_fastboot.call_count)

  def testListDevicesRemoveATFA(self):
    mock_fastboot = MagicMock()
    mock_fastboot.side_effect = self.MockInit
    atft_manager = atftman.AtftManager(mock_fastboot,
                                       self.mock_serial_mapper)
    mock_fastboot.ListDevices.return_value = [self.ATFA_TEST_SERIAL,
                                              self.TEST_SERIAL]
    atft_manager.ListDevices()
    atft_manager.ListDevices()
    mock_fastboot.ListDevices.return_value = [self.TEST_SERIAL]
    atft_manager.ListDevices()
    self.assertEqual(atft_manager.atfa_dev,
                     None)
    self.assertEqual(1, len(atft_manager.target_devs))
    self.assertEqual(atft_manager.target_devs[0].serial_number,
                     self.TEST_SERIAL)

  def testListDevicesRemoveDevice(self):
    mock_fastboot = MagicMock()
    mock_fastboot.side_effect = self.MockInit
    atft_manager = atftman.AtftManager(mock_fastboot,
                                       self.mock_serial_mapper)
    mock_fastboot.ListDevices.return_value = [self.ATFA_TEST_SERIAL,
                                              self.TEST_SERIAL]
    atft_manager.ListDevices()
    atft_manager.ListDevices()
    mock_fastboot.ListDevices.return_value = [self.ATFA_TEST_SERIAL]
    atft_manager.ListDevices()
    self.assertEqual(atft_manager.atfa_dev.serial_number,
                     self.ATFA_TEST_SERIAL)
    self.assertEqual(0, len(atft_manager.target_devs))

  def testListDevicesPendingRemove(self):
    mock_fastboot = MagicMock()
    mock_fastboot.side_effect = self.MockInit
    atft_manager = atftman.AtftManager(mock_fastboot,
                                       self.mock_serial_mapper)
    mock_fastboot.ListDevices.return_value = [self.TEST_SERIAL]
    atft_manager.ListDevices()
    # Just appear once, should not be in target device list.
    self.assertEqual(0, len(atft_manager.target_devs))

  def testListDevicesPendingAdd(self):
    mock_fastboot = MagicMock()
    mock_fastboot.side_effect = self.MockInit
    atft_manager = atftman.AtftManager(mock_fastboot,
                                       self.mock_serial_mapper)
    mock_fastboot.ListDevices.return_value = [self.TEST_SERIAL]
    atft_manager.ListDevices()
    self.assertEqual(0, len(atft_manager.target_devs))
    mock_fastboot.ListDevices.return_value = [self.TEST_SERIAL,
                                              self.TEST_SERIAL2]
    # TEST_SERIAL appears twice, should be in the list.
    # TEST_SERIAL2 just appears once, should not be in the list.
    atft_manager.ListDevices()
    self.assertEqual(1, len(atft_manager.target_devs))

  def testListDevicesPendingTemp(self):
    mock_fastboot = MagicMock()
    mock_fastboot.side_effect = self.MockInit
    atft_manager = atftman.AtftManager(mock_fastboot,
                                       self.mock_serial_mapper)
    mock_fastboot.ListDevices.return_value = [self.TEST_SERIAL]
    atft_manager.ListDevices()
    self.assertEqual(0, len(atft_manager.target_devs))
    mock_fastboot.ListDevices.return_value = [self.TEST_SERIAL2]
    atft_manager.ListDevices()
    # Nothing appears twice.
    self.assertEqual(0, len(atft_manager.target_devs))

  def testListDevicesLocation(self):
    mock_serial_mapper = MagicMock()
    mock_serial_instance = MagicMock()
    mock_serial_mapper.return_value = mock_serial_instance
    mock_serial_instance.get_serial_map.return_value = {
        self.ATFA_TEST_SERIAL: self.TEST_LOCATION,
        self.TEST_SERIAL: self.TEST_LOCATION2
    }
    mock_fastboot = MagicMock()
    mock_fastboot.side_effect = self.MockInit
    atft_manager = atftman.AtftManager(mock_fastboot,
                                       mock_serial_mapper)
    mock_fastboot.ListDevices.return_value = [self.ATFA_TEST_SERIAL,
                                              self.TEST_SERIAL]
    atft_manager.ListDevices()
    atft_manager.ListDevices()
    self.assertEqual(atft_manager.atfa_dev.location,
                     self.TEST_LOCATION)
    self.assertEqual(atft_manager.target_devs[0].location,
                     self.TEST_LOCATION2)

  # Test _SortTargetDevices
  def testSortDevicesDefault(self):
    mock_serial_mapper = MagicMock()
    mock_serial_instance = MagicMock()
    mock_serial_mapper.return_value = mock_serial_instance
    mock_serial_instance.get_serial_map.return_value = {
        self.TEST_SERIAL: self.TEST_LOCATION,
        self.TEST_SERIAL2: self.TEST_LOCATION2,
        self.TEST_SERIAL3: self.TEST_LOCATION3
    }
    mock_fastboot = MagicMock()
    mock_fastboot.side_effect = self.MockInit
    atft_manager = atftman.AtftManager(mock_fastboot,
                                       mock_serial_mapper)
    mock_fastboot.ListDevices.return_value = [self.TEST_SERIAL,
                                              self.TEST_SERIAL2,
                                              self.TEST_SERIAL3]
    atft_manager.ListDevices()
    atft_manager.ListDevices()
    self.assertEqual(3, len(atft_manager.target_devs))
    self.assertEqual(self.TEST_LOCATION, atft_manager.target_devs[0].location)
    self.assertEqual(self.TEST_LOCATION3, atft_manager.target_devs[1].location)
    self.assertEqual(self.TEST_LOCATION2, atft_manager.target_devs[2].location)

  def testSortDevicesLocation(self):
    mock_serial_mapper = MagicMock()
    mock_serial_instance = MagicMock()
    mock_serial_mapper.return_value = mock_serial_instance
    mock_serial_instance.get_serial_map.return_value = {
        self.TEST_SERIAL: self.TEST_LOCATION,
        self.TEST_SERIAL2: self.TEST_LOCATION2,
        self.TEST_SERIAL3: self.TEST_LOCATION3
    }
    mock_fastboot = MagicMock()
    mock_fastboot.side_effect = self.MockInit
    atft_manager = atftman.AtftManager(mock_fastboot,
                                       mock_serial_mapper)
    mock_fastboot.ListDevices.return_value = [self.TEST_SERIAL,
                                              self.TEST_SERIAL2,
                                              self.TEST_SERIAL3]
    atft_manager.ListDevices(atft_manager.SORT_BY_LOCATION)
    atft_manager.ListDevices(atft_manager.SORT_BY_LOCATION)
    self.assertEqual(3, len(atft_manager.target_devs))
    self.assertEqual(self.TEST_LOCATION, atft_manager.target_devs[0].location)
    self.assertEqual(self.TEST_LOCATION3, atft_manager.target_devs[1].location)
    self.assertEqual(self.TEST_LOCATION2, atft_manager.target_devs[2].location)

  def testSortDevicesSerial(self):
    mock_serial_mapper = MagicMock()
    mock_serial_instance = MagicMock()
    mock_serial_mapper.return_value = mock_serial_instance
    mock_serial_instance.get_serial_map.return_value = {
        self.TEST_SERIAL: self.TEST_LOCATION,
        self.TEST_SERIAL2: self.TEST_LOCATION2,
        self.TEST_SERIAL3: self.TEST_LOCATION3
    }
    mock_fastboot = MagicMock()
    mock_fastboot_instance = MagicMock()
    mock_fastboot.side_effect = self.MockInit
    mock_fastboot.return_value = mock_fastboot_instance
    mock_fastboot_instance.GetVar = MagicMock()
    atft_manager = atftman.AtftManager(mock_fastboot,
                                       mock_serial_mapper)
    mock_fastboot.ListDevices.return_value = [self.TEST_SERIAL2,
                                              self.TEST_SERIAL3,
                                              self.TEST_SERIAL]
    atft_manager.ListDevices(atft_manager.SORT_BY_SERIAL)
    atft_manager.ListDevices(atft_manager.SORT_BY_SERIAL)
    self.assertEqual(3, len(atft_manager.target_devs))
    self.assertEqual(self.TEST_SERIAL,
                     atft_manager.target_devs[0].serial_number)
    self.assertEqual(self.TEST_SERIAL2,
                     atft_manager.target_devs[1].serial_number)
    self.assertEqual(self.TEST_SERIAL3,
                     atft_manager.target_devs[2].serial_number)

  # Test AtftManager.TransferContent

  @staticmethod
  def _AppendFile(file_path):
    files.append(file_path)

  @staticmethod
  def _CheckFile(file_path):
    assert file_path in files
    return True

  @staticmethod
  def _RemoveFile(file_path):
    assert file_path in files
    files.remove(file_path)

  @patch('os.rmdir')
  @patch('os.remove')
  @patch('os.path.exists')
  @patch('tempfile.mkdtemp')
  @patch('uuid.uuid1')
  @patch('__main__.AtftManTest.FastbootDeviceTemplate.Upload')
  @patch('__main__.AtftManTest.FastbootDeviceTemplate.Download')
  def testTransferContentNormal(self, mock_download, mock_upload,
                                mock_uuid, mock_create_folder,
                                mock_exists, mock_remove, mock_rmdir):
    atft_manager = atftman.AtftManager(self.FastbootDeviceTemplate,
                                       self.mock_serial_mapper)
    # upload (to fs): create a temporary file
    mock_upload.side_effect = AtftManTest._AppendFile
    # download (from fs): check if the temporary file exists
    mock_download.side_effect = AtftManTest._CheckFile
    mock_exists.side_effect = AtftManTest._CheckFile
    # remove: remove the file
    mock_remove.side_effect = AtftManTest._RemoveFile
    mock_rmdir.side_effect = AtftManTest._RemoveFile
    mock_create_folder.return_value = self.TEST_TMP_FOLDER
    files.append(self.TEST_TMP_FOLDER)
    mock_uuid.return_value = self.TEST_UUID
    tmp_path = self.TEST_TMP_FOLDER + self.TEST_UUID
    src = self.FastbootDeviceTemplate(self.TEST_SERIAL)
    dst = self.FastbootDeviceTemplate(self.TEST_SERIAL)
    atft_manager.TransferContent(src, dst)
    src.Upload.assert_called_once_with(tmp_path)
    src.Download.assert_called_once_with(tmp_path)
    # we should have no temporary file at the end
    self.assertTrue(not files)

  # Test DeviceInfo.__eq__
  def testDeviceInfoEqual(self):
    test_device1 = atftman.DeviceInfo(None, self.TEST_SERIAL,
                                      self.TEST_LOCATION)
    test_device2 = atftman.DeviceInfo(None, self.TEST_SERIAL2,
                                      self.TEST_LOCATION2)
    test_device3 = atftman.DeviceInfo(None, self.TEST_SERIAL,
                                      self.TEST_LOCATION2)
    test_device4 = atftman.DeviceInfo(None, self.TEST_SERIAL2,
                                      self.TEST_LOCATION)
    test_device5 = atftman.DeviceInfo(None, self.TEST_SERIAL,
                                      self.TEST_LOCATION)
    self.assertEqual(test_device1, test_device5)
    self.assertNotEqual(test_device1, test_device2)
    self.assertNotEqual(test_device1, test_device3)
    self.assertNotEqual(test_device1, test_device4)


if __name__ == '__main__':
  unittest.main()
