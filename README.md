# Sistema de Gestão Empresarial - DER

Este sistema reflete uma estrutura empresarial bem organizada, onde diversas entidades estão interligadas para garantir uma gestão eficiente de clientes, projetos, tarefas, recursos, funcionários e departamentos. A seguir, estão as principais entidades e seus relacionamentos.

## Entidades Principais

### 1. **Clientes**
Os clientes são identificados pelo CNPJ e possuem informações essenciais como:
- **Nome**
- **Endereço**
- **Telefone**

Cada cliente pode estar associado a um ou mais **Projetos**.

### 2. **Projetos**
Os projetos são vinculados diretamente a um cliente e contêm os seguintes detalhes:
- **Nome do Projeto**
- **Descrição**
- **Datas de Início e Término**
- **Departamento Responsável**

Os projetos são compostos por várias **Tarefas**, que são geridas e possuem informações sobre seu **Status** e **Datas de Execução**.

### 3. **Contatos**
Cada cliente pode ter **Contatos**, representando indivíduos-chave, com informações como:
- **Cargo**
- **Telefone**
- **E-mail**

### 4. **Tarefas**
As tarefas são atividades específicas dentro de um projeto e possuem informações sobre:
- **Status da Tarefa**
- **Datas de Execução**

### 5. **Recursos**
Recursos são utilizados pelas tarefas e podem variar em tipo e nome. Cada recurso pode ser gerido por **Alocações**, que especificam a quantidade necessária.

### 6. **Funcionários**
Os funcionários são identificados pelo CPF e possuem as seguintes informações:
- **Nome**
- **Data de Contratação**

Os funcionários podem ser:
- **Efetivos** (com **Salário** e **Benefícios**)
- **Terceirizados** (ligados a empresas e com valores especificados por hora)

### 7. **Alocações**
As alocações são responsáveis por designar funcionários a projetos durante um período específico. Elas controlam o **Tempo** e **Quantidade** de trabalho dedicado.

### 8. **Departamentos**
Os projetos são organizados por **Departamentos**, e cada departamento tem um **Funcionário Responsável** pela gestão do mesmo, garantindo clareza e controle organizacional.

## Relacionamentos

- **Clientes** possuem **Projetos**.
- **Projetos** são compostos por **Tarefas**.
- **Tarefas** podem requerer **Recursos**, os quais são alocados por **Alocações**.
- **Funcionários** podem ser designados para projetos através de **Alocações**, controlando o tempo de dedicação.
- **Departamentos** gerenciam **Projetos** e possuem um **Responsável**.

## Como Utilizar

1. **Instale as dependências** necessárias.
2. **Configure** as entidades de acordo com as necessidades de sua organização.
3. **Acesse o sistema** para gerenciar clientes, projetos, tarefas, recursos, funcionários e departamentos.

## Contribuição

Sinta-se à vontade para contribuir para o desenvolvimento deste sistema. Caso queira adicionar novas funcionalidades ou corrigir algum erro, basta abrir uma **issue** ou enviar um **pull request**.

## Licença

Não tem licença ainda.
