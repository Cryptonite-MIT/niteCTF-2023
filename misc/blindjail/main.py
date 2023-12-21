# print(getattr("".__class__.___mro___.__subclasses__()[108])().load_module("\x6f\x73"),"")
# subclasses = "".__class__.__mro__[1].__subclasses__()
# print("Subclasses:", subclasses)


def checker(inp):
    for keyword in [
        "eval",
        "exec",
        "import",
        "open",
        "os",
        "read",
        "system",
        "write",
        "subprocess",
        "str",
        "flag",
        "import",
        "cat",
        "63",
    ]:
        if keyword in inp:
            print(f" Nope,  {keyword}  is banned! ")
            break
    else:
        o = exec(inp, {}, {})
        if o is not None:
            print(o)


print(
    "------------------------------------------------------------- \n WELCOME TO THE BLINDJAIL \n --------------------------------------------------------\n "
    "\x1B[3m fret not that you cannot see, fret that you cannot leave.\x1B[0m "
)
while True:
    try:
        inp = input(">>> ")
        if inp.lower() == "exit":
            break
        checker(inp)
    except KeyboardInterrupt:
        print("\nBye!")
        break
    except EOFError:
        print("\nBye!")
        break
    except BaseException as e:
        print("look for the light! \n", e.args)
