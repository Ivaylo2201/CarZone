const isEmpty = kwargs => !kwargs.keys().next().done;

document.getElementById('filter-form').addEventListener("submit", () => {
    event.preventDefault();

    const data = new FormData(event.target);
    const kwargs = new URLSearchParams(data);
    const cleanedKwargs = new URLSearchParams();
    let url = window.location.origin + window.location.pathname;

    for (const [key, value] of kwargs) {
        if (value) {
            cleanedKwargs.append(key, value);
        }
    }

    window.location.href = isEmpty(cleanedKwargs) ? url + '?' + cleanedKwargs.toString() : url;
})
