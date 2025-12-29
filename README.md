# verbodedeus
Portal Verbo de Deus 2025 - Django Project


# Verbo de Deus - Sistema de Gestão para ONG Cristã

Sistema completo desenvolvido em Django para a organização não governamental cristã Verbo de Deus.

## Módulos

### 1. Cadastro de Usuários
- **Perfis**: Membros, Visitantes, Produtores
- **Funções de Membros**: Curadores, Redatores, Líderes Espirituais, Revisores, Social Media, Programadores
- Sistema de permissões baseado em perfis

### 2. Livraria
- Cadastro de livros digitais (PDF, EPUB, MOBI)
- Vendas online com integração PagSeguro
- Controle de compras e downloads

### 3. Apoio Espiritual
- **Aconselhamento Pastoral**: Comunicação privada entre membros e líderes espirituais
- **Grupo de Oração**: Pedidos de oração e compromissos de intercessão

### 4. VDDFlix
- **Originais**: EBD, Devocionais, Comentando (Notícias, Livros, Artigos, Bíblia), Podcasts, Cultos
- **Plataformas**: URLs embedadas de outras plataformas
- **Cursos**: Links para cursos externos
- Sistema de favoritos/playlist para visitantes
- Comentários em conteúdos
- Sugestões de pauta

### 5. Fórum Interno
- Tópicos e respostas
- Apenas perfis específicos podem criar tópicos
- Sistema de visualizações e respostas

## Instalação

1. Clone o repositório
2. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Execute as migrações:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Crie um superusuário:
```bash
python manage.py createsuperuser
```

6. Execute o servidor:
```bash
python manage.py runserver
```

## Configuração

### Variáveis de Ambiente (Produção)
Configure as seguintes variáveis de ambiente para produção:
- `PAGSEGURO_EMAIL`: Email do PagSeguro
- `PAGSEGURO_TOKEN`: Token do PagSeguro
- `PAGSEGURO_SANDBOX`: True/False para ambiente sandbox

### Permissões por Perfil

- **Curadores**: Cadastrar, editar, revisar e excluir conteúdo do VDDFlix
- **Produtores**: Cadastrar livros, cursos e artigos
- **Redatores**: Comentários de livros, notícias, artigos, bíblia e devocionais
- **Líderes Espirituais**: Cadastrar cursos, podcasts, cultos, devocionais e EBD
- **Revisores**: Editar e apagar conteúdo do VDDFlix
- **Visitantes**: Criar playlists, comentar, sugerir pautas e solicitar aconselhamento

## Estrutura do Projeto

```
verbodedeus/
├── verbodedeus/          # Configurações do projeto
├── usuarios/             # App de usuários e perfis
├── livraria/             # App de livraria
├── apoio_espiritual/     # App de apoio espiritual
├── vdflix/               # App VDDFlix
├── forum/                # App de fórum interno
├── templates/            # Templates HTML
└── static/               # Arquivos estáticos
```

## Tecnologias Utilizadas

- Django 6.0
- CKEditor (WYSIWYG)
- Bootstrap 5
- Pillow (manipulação de imagens)
- Django Crispy Forms
- Python 3.14+ (compatível)

## Licença

Este projeto é propriedade da ONG Verbo de Deus.

