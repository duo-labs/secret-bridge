import unittest
from detectors.detectsecrets import DetectSecrets


class AttrDict(dict):
    """A hacky dictionary that exposes its members as attributes.
    Ex: attr_dict['foo'] == attr_dict.foo

    This is to mimic the way that decoded JSON objects look (i.e. JSON
    object fields are exposed attributes attributes).
    """
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


class TestDetectSecrets(unittest.TestCase):
    TEST_INPUT = """my_secret_key = "69c55daa85191f0308fc69c67dad68740a604ee957645d84101adc56b3889db1"\n"""
    TEST_JSON_OUTPUT_SUBSET = """"results": {
  "foo.txt": [
    {
      "hashed_secret": "a6846d8320dcb082eba8ab9612f8fd1df7e4a345",
      "line_number": 1,
      "type": "Hex High Entropy String"
    }
  ]
}
}"""

    def test_parse_example_output(self):
        ds = DetectSecrets()
        file_obj = AttrDict({
            "filename": "secret_test.txt",
            "patch": self.TEST_INPUT
        })
        out = ds.run('tmp_path', file_obj)
        self.assertEqual(len(out), 1)
        finding = out[0]
        self.assertEqual(finding.secret_type, "Hex High Entropy String")
