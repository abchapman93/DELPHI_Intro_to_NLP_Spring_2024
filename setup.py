from setuptools import setup, find_packages
import os


# function to recursively get files for resourcee
def package_files(directory):
   paths = []
   for (p, directories, filenames) in os.walk(directory):
      for filename in filenames:
         paths.append(os.path.join("..", p, filename))
   return paths



setup(
   name='delphi_nlp_2024',
   version='0.1',
   description='Python package to help with DELPHI 2024 NLP workshop.',
   author='Alec Chapman',
   author_email='abchapman93@gmail.com',
   packages=["delphi_nlp_2024", "delphi_nlp_2024.quizzes"],  #same as name
   package_dir={"delphi_nlp_2024": "delphi_nlp_2024",
                "delphi_nlp_2024.quizzes": "delphi_nlp_2024/quizzes"},
   install_requires=['jupyter'], #external packages as dependencies
)