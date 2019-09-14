class Finding:
    def __init__(self, filename, secret_type, secret_value, line_number=None, link=None):
        self._filename = filename
        self._secret_type = secret_type
        self._secret_value = secret_value
        self._line_number = line_number
        self._link = link

    @property
    def filename(self):
        return self._filename

    @property
    def secret_type(self):
        return self._secret_type

    @property
    def link(self):
        return self._link

    @property
    def line_number(self):
        return self._line_number

    def __eq__(self, other):
        if isinstance(other, Finding):
            return self.filename == other.filename and \
                   self.secret_type == other.secret_type and \
                   self._secret_value == other._secret_value

    def __hash__(self):
        return hash((self._filename, self._secret_type, self._secret_value))

    def __str__(self):
        s = "Secret type {} found in {}".format(self._secret_type, self._filename)
        if self._line_number is not None:
            s = s + ":{}".format(self._line_number)
        if self._link is not None:
            s = s + " ({})".format(self._link)
        return s

    def __repr__(self):
        return "<{}> ({})".format(self._secret_type, self._filename)
