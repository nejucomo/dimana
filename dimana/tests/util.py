def ParseTestClass(testcls):
    make_title = lambda s: repr(str(s).replace('.', '_'))
    cls = testcls.targetclass

    def set_tests(value, text, alts):
        title = make_title(value)

        # This exists merely to work around loop scoping issue.
        setattr(
            testcls,
            'test_str_of {}'.format(title),
            lambda self: self.assertEqual(text, str(value)),
        )

        repexp = '<{} {!r}>'.format(cls.__name__, text)
        setattr(
            testcls,
            'test_repr_of {}'.format(title),
            lambda self: self.assertEqual(repexp, repr(value)),
        )

        texts = [text] + alts
        setattr(
            testcls,
            'test_parse_of {}'.format(title),
            lambda self: [
                self.assertEqual(value, cls.parse(t))
                for t
                in texts
            ],
        )

    for (value, text, alts) in testcls.cases:
        set_tests(value, text, alts)

    for badinput in testcls.errorcases:
        setattr(
            testcls,
            'test_parse_error_of {!r}'.format(make_title(badinput)),
            lambda self: self.assertRaises(
                cls.ParseError,
                cls.parse,
                badinput,
            )
        )

    return testcls
