import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

@anvil.server.portable_class
class String:

    @staticmethod
    def fit_length(string, length):
        fitted = []
        result = ""
        count = 0
        for symbol in str(string):
            result += symbol
            count += 1
            if count >= length:
                result = result.center(50, " ")
                result += "\n"
                fitted.append(result)
                count = 0
                result = ""
        result = result.center(50, " ")
        fitted.append(result)
        result = ""
        for part in fitted:
            result += part
        return result

    @staticmethod
    def slash_to_back_slash(string):
        out = ""
        for symbol in str(string):
            if symbol == "\\" or symbol == "\\\\":
                out += "/"
            else:
                out += symbol
        return out

    @staticmethod
    def back_slash_to_double_slash(string):
        out = ""
        for symbol in str(string):
            if symbol == "/":
                out += "\\"
            else:
                out += symbol
        return out

    @staticmethod
    def remove_brackets(string):
        out = ""
        for symbol in string:
            if symbol in ("(", ")", "[", "]", "{", "}"):
                pass
            else:
                out += symbol
        return out

    @staticmethod
    def fit_url(url="www.google.com"):
        """
        "www.google.com/search=None"
        ("http://google.com/search=None", "google.com", "http://google.com")
        """
        if not url.startswith("http"):
            protocol = "https://"
        else:
            protocol = url.split("//")[0] + "//"
        url = url.replace("http://", "").replace("https://", "").replace("www.", "")
        site = url.split("/")[0].strip()
        return (protocol + url), site, (protocol + site)

    @staticmethod
    def get_similarity(str1, str2):
      str1 = str1 + ' ' * (len(str2) - len(str1))
      str2 = str2 + ' ' * (len(str1) - len(str2))
      return int(sum(1 if i == j else 0 for i, j in zip(str1, str2)) / float(len(str1))*100)

