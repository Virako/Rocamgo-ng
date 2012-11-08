class Ruleset:
    _rulesets = (
        {'Japanese':
            ({'komi': "6.5", 'allow_suicide': False, 'superko': False}),
        'Chinese':
            ({'komi': "7.5", 'allow_suicide': False, 'superko': "positional"}),
        'AGA':
            ({'komi': "7.5", 'allow_suicide': False, 'superko': "situational"})
    })

    @classmethod
    def get_available(rs):
        return rs._rulesets.keys()

    @classmethod
    def get(rs, ruleset):
        return rs._rulesets.values(ruleset)
