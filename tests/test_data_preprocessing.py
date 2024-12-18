import unittest
from data_preprocessing import normalize_salary, split_address, normalize_job_title

class TestNormalizeSalary(unittest.TestCase):
    def test_salary_range(self):
        self.assertEqual(normalize_salary('10-20 triệu VND'), (10, 20, 'VND'))

    def test_fixed_salary(self):
        self.assertEqual(normalize_salary('15 triệu VND'), (15, 15, 'VND'))

    def test_invalid_salary(self):
        self.assertEqual(normalize_salary('Thỏa thuận'), (None, None, None))
        self.assertEqual(normalize_salary(None), (None, None, None))

    def test_different_currency(self):
        self.assertEqual(normalize_salary('1000-2000 $'), (1000, 2000, 'USD'))

class TestSplitAddress(unittest.TestCase):
    def test_valid_address(self):
        self.assertEqual(split_address('Quận 1, TP Hồ Chí Minh'), ('Quận 1', 'TP Hồ Chí Minh'))

    def test_missing_district(self):
        self.assertEqual(split_address('TP Hồ Chí Minh'), (None, 'TP Hồ Chí Minh'))

    def test_invalid_address(self):
        self.assertEqual(split_address(None), (None, None))
        self.assertEqual(split_address(''), (None, None))


class TestNormalizeJobTitle(unittest.TestCase):
    def test_normal_title(self):
        self.assertEqual(normalize_job_title('Python Developer'), 'Developer')

    def test_title_with_spaces(self):
        self.assertEqual(normalize_job_title('   Data Scientist   '), 'Other')  # Không khớp từ khóa, trả về Other

    def test_title_with_special_characters(self):
        self.assertEqual(normalize_job_title('AI/ML Engineer!'), 'Engineer')

    def test_intern_title(self):
        self.assertEqual(normalize_job_title('Intern Python'), 'Intern')

    def test_invalid_title(self):
        self.assertEqual(normalize_job_title(None), 'Other')
        self.assertEqual(normalize_job_title(''), 'Other')



if __name__ == '__main__':
    unittest.main()