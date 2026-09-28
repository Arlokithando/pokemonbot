import aiohttp  # Eşzamansız HTTP istekleri için bir kütüphane
import random

class Pokemon:
    pokemons = {}
    # Nesne başlatma (kurucu)
    def __init__(self, pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer
        self.pokemon_number = random.randint(1, 1000)
        self.name = None
        self.power = random.randint(30,60)
        self.hp = random.randint(200,400)
        if pokemon_trainer not in Pokemon.pokemons:
            Pokemon.pokemons[pokemon_trainer] = self
        else:
            self = Pokemon.pokemons[pokemon_trainer]

    async def get_name(self):
        # PokeAPI aracılığıyla bir pokémonun adını almak için asenktron metot
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'  # İstek için URL API
        async with aiohttp.ClientSession() as session:  #  HTTP oturumu açma
            async with session.get(url) as response:  # GET isteği gönderme
                if response.status == 200:
                    data = await response.json()  # JSON yanıtının alınması ve çözümlenmesi
                    return data['forms'][0]['name']  #  Pokémon adını döndürme
                else:
                    return "Pikachu"  # İstek başarısız olursa varsayılan adı döndürür

    async def info(self):
        # Pokémon hakkında bilgi döndüren bir metot
        if not self.name:
            self.name = await self.get_name()  # Henüz yüklenmemişse bir adın geri alınması
        return f"Pokémonunuzun ismi: {self.name}"  # Pokémon adını içeren dizeyi döndürür

    async def show_img(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'  # İstek için URL API

        async with aiohttp.ClientSession() as session:  #  HTTP oturumu açma
                    async with session.get(url) as response:  # GET isteği gönderme
                        if response.status == 200:
                            data = await response.json()
                            return data ["sprites"]["front_default"]
                        else: return None
    async def attack(self,enemy):
         if enemy.hp > self.power:
              enemy.hp -= self.power
              return f"Pokémon eğitmeni @{self.pokemon_trainer} @{enemy.pokemon_trainer}'ne saldırdı\n@{enemy.pokemon_trainer}'nin sağlık durumu {enemy.hp}"
         else:
              enemy.hp = 0
              return f"Pokémon eğitmeni @{self.pokemon_trainer} @{enemy.pokemon_trainer}'ni yendi!"
class Wizzard(Pokemon):
     pass

class Fighter(Pokemon):
    async def attack (self,enemy):
         superpower = random.randint(5,15)
         self.power += superpower
         result = await super().attack(enemy)
         self.power -= superpower
         return result + f"\nDövüşçü Pokémon süper saldırı kullandı. Eklenen güç: {superpower}"
