# Install web driver (mac) for firefox

Uses geckodriver

instructions used from https://blog.finxter.com/how-to-solve-webdriverexception-message-geckodriver-executable-needs-to-be-in-path/

## 1. Home brew

"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

## 2. Geckodriver

brew install geckodriver

### locate

copy this -> where geckodriver
(returns this for me: /opt/homebrew/bin/geckodriver)

## 3. Set as driver param

driver = webdriver.Firefox(executable_path='/opt/homebrew/bin/geckodriver')
** Note executable_path is deprecated and uses Service(<path>) 
