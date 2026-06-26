const params = new URLSearchParams(window.location.search);
const comicId = params.get("id");

const titleElement = document.getElementById("comicTitle");
const readerElement = document.getElementById("reader");
const backButton = document.getElementById("backButton");

backButton.onclick = () => {
    history.back();
};

start();

async function start() {

    if (!comicId) {

        readerElement.innerHTML = `
            <div id="loading">
                Comic ID not found.
            </div>
        `;

        return;
    }

    try {

        const library = await ComicAPI.loadLibrary();

        const comic = library.library.find(
            item => String(item.uid) === comicId
        );

        if (!comic) {

            readerElement.innerHTML = `
                <div id="loading">
                    Comic not found.
                </div>
            `;

            return;
        }

        titleElement.textContent =
            comic.title.display;

        await loadComic(comic.file);

    }

    catch (error) {

        console.error(error);

        readerElement.innerHTML = `
            <div id="loading">
                Failed to load comic.
            </div>
        `;

    }

}

async function loadComic(filename) {

    readerElement.innerHTML = `
        <div id="loading">
            Opening CBZ...
        </div>
    `;

    const response = await fetch(
        `comics/${filename}`
    );

    if (!response.ok) {

        throw new Error(
            "Unable to download CBZ."
        );

    }

    const buffer =
        await response.arrayBuffer();

    const zip =
        await JSZip.loadAsync(buffer);

    const files = [];

    zip.forEach((path, file) => {

        if (file.dir)
            return;

        const lower =
            path.toLowerCase();

        if (
            lower.endsWith(".webp") ||
            lower.endsWith(".jpg") ||
            lower.endsWith(".jpeg") ||
            lower.endsWith(".png")
        ) {

            files.push(file);

        }

    });

    files.sort((a, b) => {

        return a.name.localeCompare(
            b.name,
            undefined,
            {
                numeric: true
            }
        );

    });

    readerElement.innerHTML = "";

    for (const file of files) {

        const blob =
            await file.async("blob");

        const url =
            URL.createObjectURL(blob);

        const page =
            document.createElement("div");

        page.className = "page";

        const image =
            document.createElement("img");

        image.loading = "lazy";

        image.src = url;

        image.draggable = false;

        page.appendChild(image);

        readerElement.appendChild(page);

    }

}
