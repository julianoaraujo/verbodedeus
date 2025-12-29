# Guia de Configuração - Verbo de Deus

## Passo a Passo para Iniciar o Projeto

### 1. Preparação do Ambiente

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

### 2. Configuração do Banco de Dados

```bash
# Criar migrações
python manage.py makemigrations

# Aplicar migrações
python manage.py migrate
```

### 3. Criar Superusuário

```bash
python manage.py createsuperuser
```

Siga as instruções para criar o primeiro usuário administrador.

### 4. Coletar Arquivos Estáticos (Produção)

```bash
python manage.py collectstatic
```

### 5. Executar o Servidor

```bash
python manage.py runserver
```

Acesse: http://127.0.0.1:8000

## Configuração Inicial Recomendada

### 1. Criar Linhas Teológicas

Após fazer login como administrador, acesse o painel admin e crie as linhas teológicas que serão usadas no sistema:
- Reformada
- Pentecostal
- Batista
- Presbiteriana
- etc.

### 2. Criar Usuários de Teste

Crie usuários com diferentes perfis para testar as funcionalidades:
- Visitante
- Membro com perfil de Curador
- Membro com perfil de Líder Espiritual
- Membro com perfil de Redator
- etc.

### 3. Configurar PagSeguro (Produção)

No arquivo `verbodedeus/settings.py` ou usando variáveis de ambiente:

```python
PAGSEGURO_EMAIL = 'seu-email@exemplo.com'
PAGSEGURO_TOKEN = 'seu-token'
PAGSEGURO_SANDBOX = True  # False em produção
```

## Estrutura de Permissões

### Visitantes podem:
- Criar playlists (favoritos)
- Comentar em notícias, artigos, devocionais
- Sugerir pautas
- Solicitar aconselhamento pastoral

### Membros podem (dependendo do perfil):
- **Curadores**: Cadastrar, editar, revisar e excluir conteúdo VDDFlix
- **Produtores**: Cadastrar livros, cursos e artigos
- **Redatores**: Comentários de livros, notícias, artigos, bíblia e devocionais
- **Líderes Espirituais**: Cadastrar cursos, podcasts, cultos, devocionais e EBD
- **Revisores**: Editar e apagar conteúdo do VDDFlix
- **Social Media**: Cadastrar posts no fórum
- **Programadores**: Cadastrar posts no fórum

## Próximos Passos

1. Personalizar templates conforme necessário
2. Configurar servidor de produção
3. Configurar domínio e SSL
4. Implementar backup automático do banco de dados
5. Configurar monitoramento e logs

