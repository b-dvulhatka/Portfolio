document.addEventListener("DOMContentLoaded", () => {
    const grid = document.getElementById("portfolio-grid");
    const loading = document.getElementById("loading");

    fetch('./projetos.json')
        .then(response => {
            if (!response.ok) throw new Error("Arquivo de dados não encontrado.");
            return response.json();
        })
        .then(projetos => {
            loading.style.display = 'none'; // Esconde o aviso de carregamento
            
            projetos.forEach(projeto => {
                const card = document.createElement("div");
                card.className = "card";
                
                const dataFormatada = new Date(projeto.atualizado_em).toLocaleDateString('pt-BR');
                
                card.innerHTML = `
                    <span class="badge ${projeto.origem.toLowerCase()}">${projeto.origem}</span>
                    <h3>${projeto.titulo}</h3>
                    <p class="descricao">${projeto.descricao}</p>
                    <p class="tech-stack">${projeto.tecnologias}</p>
                    <p class="date">Atualizado em: ${dataFormatada}</p>
                    <a href="${projeto.url}" target="_blank">Acessar Código &rarr;</a>
                `;
                
                grid.appendChild(card);
            });
        })
        .catch(erro => {
            console.error("Erro:", erro);
            loading.innerText = "Nenhum projeto encontrado ou erro ao carregar os dados.";
        });
});