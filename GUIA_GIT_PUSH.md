# Guia Rápido de Git

Este guia mostra como registrar e enviar as mudanças do projeto para o GitHub.

---

## 1. Verificar o Estado Atual

```bash
git status
```

Confira quais arquivos foram modificados, movidos ou criados.

---

## 2. Adicionar Arquivos

Para adicionar tudo que deve entrar no commit:

```bash
git add .
```

Se quiser adicionar por partes:

```bash
git add README.md
git add checklist_semanal/
git add notebooks/
git add instrucoes_IC/
git add relatorio/
```

---

## 3. Fazer Commit

Use uma mensagem curta e clara:

```bash
git commit -m "docs: atualizar estrutura do projeto"
```

Outros exemplos:

```bash
git commit -m "feat: adicionar notebook de comparacao da semana 3"
git commit -m "docs: adicionar checklist e relatorio da semana 3"
git commit -m "docs: atualizar plano de inteligencia computacional"
git commit -m "fix: corrigir caminhos dos notebooks"
```

---

## 4. Enviar para o GitHub

```bash
git push
```

---

## Arquivos que Não Devem Subir

O arquivo abaixo deve ficar apenas local:

```text
dados/creditcard.csv
```

Motivo:

- é grande;
- contém dados;
- já deve ser ignorado pelo `.gitignore`.

---

## Estrutura que Deve Aparecer no GitHub

```text
README.md
INICIO_AQUI.md
GUIA_GIT_PUSH.md
PROBLEMA.md
RESUMO_ARQUIVOS_CRIADOS.md
checklist_semanal/
instrucoes_IC/
notebooks/
scripts/
relatorio/
```

---

## Checagem Final Antes do Push

- [ ] `git status` revisado
- [ ] `dados/creditcard.csv` não está no commit
- [ ] notebooks abrem corretamente
- [ ] relatórios semanais estão revisados
- [ ] caminhos nos arquivos Markdown estão atualizados
- [ ] mensagem de commit está clara
- [ ] `git push` executado

---

## Problemas Comuns

**Erro: `fatal: not a git repository`**  
Abra o terminal dentro da pasta `fraud-detection`.

**Erro de autenticação no GitHub**  
Confira credenciais, token pessoal ou login do GitHub.

**CSV apareceu no commit**  
Remova do stage antes do commit:

```bash
git restore --staged dados/creditcard.csv
```

---

**Status:** guia atualizado para a estrutura atual do projeto.
