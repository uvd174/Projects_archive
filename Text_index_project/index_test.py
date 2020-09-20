import unittest
import index


class IndexTests(unittest.TestCase):
    def test_make_word_list(self):
        self.assertEqual(index.make_word_list('!NotРаботает почему-то.'), ['работает', 'почему-то'])
        self.assertEqual(index.make_word_list(''), [])
        self.assertEqual(index.make_word_list('asd234#$%/*+;;'), [])
        self.assertEqual(index.make_word_list('wСoЛrОdВsА'), ['с', 'л', 'о', 'в', 'а'])
        self.assertEqual(index.make_word_list('Так точно-с, так-то'), ['так', 'точно-с', 'так-то'])
        self.assertEqual(index.make_word_list('--оп, - ЛУЧШЕ!!'), ['--оп', '-', 'лучше'])

    def test_hyphen_check(self):
        self.assertEqual(index.hyphen_check('точно-с'), 'точно')
        self.assertEqual(index.hyphen_check('--'), '')
        self.assertEqual(index.hyphen_check('а-а-а-а'), '')
        self.assertEqual(index.hyphen_check('ав-'), '')
        self.assertEqual(index.hyphen_check('светло-голубой'), 'светло-голубой')
        self.assertEqual(index.hyphen_check('работает'), 'работает')
        self.assertEqual(index.hyphen_check('-пам-'), '')
        self.assertEqual(index.hyphen_check('кое-кто'), 'кое-кто')


if __name__ == '__main__':
    unittest.main()
