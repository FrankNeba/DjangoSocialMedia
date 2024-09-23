const data = document.currentScript.dataset
const page = data.page
const links = document.querySelectorAll('.link')

links.forEach(link => {
    if(link.getAttribute('data-url-name') === page){
        link.classList.add('text-primary')
    }
})