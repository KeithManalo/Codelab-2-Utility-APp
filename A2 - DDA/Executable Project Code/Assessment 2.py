import tkinter as tk
import requests
from PIL import Image, ImageTk
from io import BytesIO

#class to store information
class Pokemon:
    def __init__(self, name, height, weight, description, image_url):
        self.name=name
        self.height=height
        self.weight=weight
        self.description=description
        self.image_url=image_url

    #class to get data from api
    @classmethod
    def fetch_pokemon(cls, identifier):
        url=f"https://pokeapi.co/api/v2/pokemon/{identifier}"
        response=requests.get(url)
        if response.status_code == 200:
            data=response.json()
            name=data['name']
            height=data['height']
            weight=data['weight']
            description=cls.get_description(data['species']['url'])
            image_url=data['sprites']['front_default']
            return cls(name, height, weight, description, image_url)
        return None

    #for pokemon description
    @staticmethod
    def get_description(species_url):
        response=requests.get(species_url)
        if response.status_code == 200:
            species_data=response.json()
            return species_data['flavor_text_entries'][0]['flavor_text']
        return "No description available."

    #fir fetching list
    @staticmethod
    def fetch_all_pokemon():
        all_pokemon=[]
        url="https://pokeapi.co/api/v2/pokemon?limit=1000"
        response=requests.get(url)
        if response.status_code == 200:
            data=response.json()
            all_pokemon=[pokemon['name'] for pokemon in data['results']]
        return sorted(all_pokemon)

# Class to create the Pokémon application GUI
class PokemonApp:
    def __init__(self, root):
        self.root=root
        self.root.title("PokeRecord Archive")
        
        #label and entry for input user
        self.label=tk.Label(root, text="Input Pokemon Name or ID:",font=("overlock",12), bg="lightblue")
        self.label.pack(padx=10, pady=5)
        self.entry=tk.Entry(root,font=("overlock",12))
        self.entry.pack(pady=5)

        #search button
        self.search_button=tk.Button(root, text="Search", command=self.search_pokemon, bg="lightgray",font=("overlock",10))
        self.search_button.pack(pady=5)

        #button to show all pokemon
        self.all_pokemon_button=tk.Button(root, text="Show All Pokémon", command=self.show_all_pokemon, bg="lightgray",font=("overlock",10))
        self.all_pokemon_button.pack(pady=5)

        #label to display result
        self.result_label=tk.Label(root, text="", bg="lightblue",font=("overlock",12))
        self.result_label.pack(pady=5)

        #label to display img
        self.image_label=tk.Label(root , bg="lightblue")
        self.image_label.pack(pady=5)

    # pokemon searcher for user input
    def search_pokemon(self):
        identifier=self.entry.get()  
        pokemon=Pokemon.fetch_pokemon(identifier)
        if pokemon:
            self.result_label.config(text=f"Name: {pokemon.name}\nHeight: {pokemon.height}\nWeight: {pokemon.weight}\nDescription: {pokemon.description}")
            self.display_image(pokemon.image_url)
        else:
            self.result_label.config(text="No Pokemon Result")

    #displaying pokemon image
    def display_image(self, image_url):
        response=requests.get(image_url)
        img_data=Image.open(BytesIO(response.content))
        img_data = img_data.resize((200, 200))
        img=ImageTk.PhotoImage(img_data)
        self.image_label.config(image=img)
        self.image_label.image=img

    #to display the list of pokemon
    def show_all_pokemon(self):
        all_pokemon=Pokemon.fetch_all_pokemon()
        self.display_pokemon_list(all_pokemon)
    #new window for pokemon list
    def display_pokemon_list(self, pokemon_list):
        list_window=tk.Toplevel(self.root)
        list_window.title("Pokemon Names (A-Z)")
        
        #scrollbar
        scrollbar=tk.Scrollbar(list_window)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        #listboxt for the names
        listbox=tk.Listbox(list_window, width=50, height=30,font=("overlock",10), yscrollcommand=scrollbar.set)
        for pokemon in pokemon_list:
            listbox.insert(tk.END, pokemon)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH)
        scrollbar.config(command=listbox.yview)
        listbox.bind('<Double-1>', lambda event: self.on_pokemon_click(listbox))

    #to click the name in the list
    def on_pokemon_click(self, listbox):
        selected_index=listbox.curselection()
        if selected_index:
            selected_pokemon=listbox.get(selected_index)
            self.entry.delete(0, tk.END)
            self.entry.insert(0, selected_pokemon)
            self.search_pokemon()

#running the application
if __name__ == "__main__":
    root=tk.Tk()
    root.geometry("800x500")
    root.configure(bg="lightblue")
    app=PokemonApp(root)  
    root.mainloop()  