from dotenv import load_dotenv
from gpt_util import GptService

load_dotenv()

prompt = '''
Provide information about Poland in the JSON format like so:
{
    "capital": <name of capital city>
    "population": <population of the country>
    "language": <official language used in the country>
}
'''

# works when run as: python -m w3.t2.packages_and_imports from the root dir (don't need to create __init__ because root dir is auto added to sys.path which allows finding this module)
# IF I wanted to move it to ./utils directory, then I would need to mark it as a package and then import it as: from utils.gpt_util import GptService
#
# sys.path: By default, it includes the directory from which you run the script or module, but you can modify it if needed.
#
# __init__.py: While it can be an empty file to mark a directory as a package, you can also use it to run initialization code, 
#   import submodules, define package-level variables, or control what is exposed to users of the package through the __all__ list.
# 
# by adding to __init__ file in utils package: from .gpt_util import GptService
# the import would change from: from utils.gpt_util import GptService ---> from utils import GptService
# ALSO in this file you can add __all__ = ['GptService'] so that if there are other modules in the package only this one will be available for import
# for multiple: 
#   from .gpt_util import GptService
#   from .whisper_util import WhisperService
#   __all__ = ['GptService', 'WhisperService']
# then in some script: from utils import GptService, WhisperService
gpt = GptService()
response = gpt.user_completion_json(prompt, temperature=1.0)

print(response)