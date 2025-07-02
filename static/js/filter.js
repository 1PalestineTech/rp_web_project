const API_BASE_URL = window.location.origin;
async function filter(){
    title = document.querySelector(".search_article").value;
    tag = document.querySelector(".tags_values").value;
    csrfToken = document.getElementById("csrf_token").value;
    fetch(`${API_BASE_URL}/filter`, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({tags:tag,name:title}),
    }).then(response => response.json()).then(result =>{
        articles = document.querySelector(".articles_group");
        articles.innerHTML=""
        is_admin=result["data"]
        for (article of result["data"]){
            console.log(article[4])
            let element = `<div class="article" id="article_${article[0]}">
                    <div>
                        <figure>
                            <img src="/static/cover.png" alt="${article[1]}">
                        
                    
                        </figure>
                    </div>
                    <div class="article_items">
                        <h4><a href="article/${article[0]}">${article[1]}</a></h4>
                        <p>${article[2]}</p>
                        <p>${article[3]}</p>
                        ${ is_admin ? `<div><a href="edit/${article[0]}"><button class="submit_btn">Edit</button></a> <button class="delete_btn" onclick="delete_article('${article[0]}')">Delete</button></div>`: ""}
                    </div>
                    </div>`
                    articles.innerHTML += element
        }
    });

}
