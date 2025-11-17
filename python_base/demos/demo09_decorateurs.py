def mon_decorateur(fct):
    def wrap_fct():
        print("Code avant")
        fct()
        print("Code après")
    return wrap_fct

@mon_decorateur
def fct():
    print("Code pendant")

fct()