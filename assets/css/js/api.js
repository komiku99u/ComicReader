class ComicAPI {

    static async loadLibrary() {

        const response = await fetch("data/library.json");

        if (!response.ok) {
            throw new Error("Failed to load library.json");
        }

        return await response.json();
    }

}