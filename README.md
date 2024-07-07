# Lambda - Faas Delete User Data

Este repositório contém a implementação de uma função AWS Lambda para excluir dados de usuários conforme a LGPD (Lei Geral de Proteção de Dados) e GDPR (Regulamento Geral sobre a Proteção de Dados). A função Lambda é provisionada utilizando Terraform e integra com o Amazon API Gateway.

## Estrutura do Projeto

- `app`: Implementação da lógica dos requisitos.
- `infra`: Arquivos do terraform para provisionar os recursos na AWS.

## Pré-requisitos

1. [Terraform](https://www.terraform.io/downloads.html) instalado.
2. AWS CLI configurado com as credenciais apropriadas.
3. Python 3.8 ou superior instalado para desenvolvimento das funções Lambda.

## Configuração

### 1. Instale o Terraform

Se você ainda não tem o Terraform instalado, siga as instruções no [site oficial do Terraform](https://www.terraform.io/downloads.html).

### 2. Prepare o Arquivo ZIP da Função Lambda

Certifique-se de que você tenha o arquivo zipado da função Lambda (`gdpr_compliant_user_deletion.zip`) no mesmo diretório do arquivo `main.tf` ou ajuste os caminhos conforme necessário.

### 3. Inicialize o Terraform

No diretório onde o arquivo `main.tf` está localizado, execute o seguinte comando para inicializar o Terraform:

```sh
terraform init
```


### 4. Visualize o Plano de Execução

Visualize o plano de execução para verificar as alterações que o Terraform fará na sua infraestrutura:

```sh
terraform plan
```

### 5. Aplique a Configuração

Aplique a configuração para provisionar os recursos:


```sh
terraform apply
```
Digite yes quando solicitado para confirmar a execução.

