from PyPDF2 import PdfReader
import re
import os
from typing import Dict, List, Optional

class LicitacaoReader:
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        
    def read_pdf(self) -> str:
        """Lê o arquivo PDF e retorna todo o texto."""
        try:
            with open(self.pdf_path, 'rb') as file:
                # Criar um objeto PDF reader
                pdf_reader = PdfReader(file)
                
                # Extrair texto de todas as páginas
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
                    
                return text
        except Exception as e:
            print(f"Erro ao ler o PDF: {e}")
            return ""

    def extract_machine_specs(self, text: str) -> List[Dict[str, str]]:
        """Extrai especificações das máquinas do texto."""
        machines = []
        
        # Primeiro, identificar os itens completos
        item_pattern = r'Item \d+ - Trator.*?(?=Item \d+ -|$)'
        items = re.finditer(item_pattern, text, re.DOTALL)
        
        for item_match in items:
            item_text = item_match.group(0)
            if not item_text.strip():
                continue
            
            item = {}
            
            # Tentar diferentes padrões de especificações
            specs_patterns = [
                # Padrão 1 (original)
                (
                    r'Trator Tipo:\s*(Microtrator/Motocultivador).*?'
                    r'Potência:\s*(\d+CV).*?'
                    r'Tipo Motor:\s*(Monocilíndrico).*?'
                    r'Motor\s+(\d+)\s+Tempos.*?'
                    r'Tipo Uso:\s*(Agrícola).*?'
                    r'Características Adicionais:\s*(.*?)(?=\n|$)'
                ),
                # Padrão 2 (novo formato)
                (
                    r'Trator Tipo:\s*(Microtrator).*?'
                    r'Potência:\s*(\d+CV).*?'
                    r'Tipo Combustível:\s*(Diesel).*?'
                    r'Tipo Motor:\s*(\d+ Tempos\s*[^,\n]*)'
                )
            ]
            
            # Tentar cada padrão até encontrar um que funcione
            for pattern in specs_patterns:
                specs_match = re.search(pattern, item_text, re.DOTALL | re.IGNORECASE)
                if specs_match:
                    # Padrão 1
                    if len(specs_match.groups()) == 6:
                        item['tipo_equipamento'] = specs_match.group(1)
                        item['potencia'] = specs_match.group(2)
                        item['tipo_motor'] = specs_match.group(3)
                        item['tempos_motor'] = specs_match.group(4)
                        item['tipo_uso'] = specs_match.group(5)
                        item['caracteristicas_adicionais'] = specs_match.group(6).strip()
                        break
                    # Padrão 2
                    elif len(specs_match.groups()) == 4:
                        item['tipo_equipamento'] = specs_match.group(1)
                        item['potencia'] = specs_match.group(2)
                        item['tipo_combustivel'] = specs_match.group(3)
                        item['tipo_motor'] = specs_match.group(4)
                        item['tipo_uso'] = 'Agrícola'  # Valor padrão para este modelo
                        break
            
            # Extrair informações do edital
            item['quantidade'] = int(re.search(r'Quantidade:\s*(\d+)', item_text).group(1))
            
            # Tentar diferentes padrões para valores
            # Padrão 1 (original)
            valor_unitario = re.search(r'Valor estimado:\s*R\$\s*([\d.,]+)', item_text)
            if not valor_unitario:
                # Padrão 2 (novo formato)
                valor_unitario = re.search(r'Valor estimado:\s*R\$\s*([\d.,]+)\s*\(unitário\)', item_text)
            if valor_unitario:
                item['valor_unitario'] = float(valor_unitario.group(1).replace('.', '').replace(',', '.'))
            
            # Padrão 1 (original)
            valor_total = re.search(r'R\$\s*([\d.,]+)\s*\(total\)', item_text)
            if not valor_total:
                # Padrão 2 (novo formato)
                valor_total = re.search(r'R\$\s*([\d.,]+)\s*\(total\)', item_text)
            if valor_total:
                item['valor_total'] = float(valor_total.group(1).replace('.', '').replace(',', '.'))
            
            # Tentar diferentes padrões para situação
            situacao_patterns = [
                r'Situação:\s*(.*?)(?=\n|$)',
                r'Situação:\s*(Aguardando adjudicação)',
                r'Situação:\s*(Aberto para recursos)'
            ]
            
            for pattern in situacao_patterns:
                situacao = re.search(pattern, item_text)
                if situacao:
                    item['situacao'] = situacao.group(1).strip()
                    break
            
            # Critério de julgamento
            criterio = re.search(r'Critério de julgamento:\s*(.*?)(?=\n|$)', item_text)
            if criterio:
                item['criterio_julgamento'] = criterio.group(1).strip()
            
            # Tratamento diferenciado (se existir)
            tratamento = re.search(r'Tratamento Diferenciado ME/EPP:\s*(.*?)(?=\n|$)', item_text)
            if tratamento:
                item['tratamento_diferenciado'] = tratamento.group(1).strip()
            
            machines.append(item)
        
        return machines

    def process_edital(self) -> Optional[List[Dict[str, str]]]:
        """Processa o edital completo e retorna as informações estruturadas."""
        # Ler o PDF
        text = self.read_pdf()
        if not text:
            return None
            
        # Extrair especificações
        return self.extract_machine_specs(text)

def processar_arquivo(pdf_path: str) -> bool:
    """Processa um arquivo PDF e retorna True se foi processado com sucesso."""
    try:
        reader = LicitacaoReader(pdf_path)
        results = reader.process_edital()
        
        if not results:
            print("Não foi possível processar o edital.")
            return False
        
        # Mostra os resultados
        print("\nInformações do Edital na ordem solicitada:")
        for item in results:
            print("\nEspecificações do Equipamento:")
            print(f"1. Tipo do equipamento: {item.get('tipo_equipamento', 'Não especificado')}")
            print(f"2. Potência: {item.get('potencia', 'Não especificado')}")
            print(f"3. Tipo do motor: {item.get('tipo_motor', 'Não especificado')}")
            print(f"4. Tempos do motor: {item.get('tempos_motor', 'Não especificado')}")
            print(f"5. Tipo de uso: {item.get('tipo_uso', 'Não especificado')}")
            print(f"6. Características adicionais: {item.get('caracteristicas_adicionais', 'Não especificado')}")
            
            print("\nInformações do Edital:")
            print(f"7. Quantidade: {item.get('quantidade', 'Não especificado')}")
            if 'valor_unitario' in item:
                print(f"8. Valor unitário: R$ {item['valor_unitario']:,.4f}")
            if 'valor_total' in item:
                print(f"9. Valor total: R$ {item['valor_total']:,.4f}")
            print(f"10. Situação: {item.get('situacao', 'Não especificado')}")
            print(f"11. Critério de julgamento: {item.get('criterio_julgamento', 'Não especificado')}")
            print(f"12. Tratamento diferenciado: {item.get('tratamento_diferenciado', 'Não especificado')}")
        return True
        
    except Exception as e:
        print(f"Erro ao processar o arquivo: {str(e)}")
        return False

def main():
    while True:
        try:
            # Solicita o caminho do arquivo ao usuário
            print("\nDigite o caminho completo do arquivo PDF (ou 'sair' para encerrar):")
            pdf_path = input().strip().replace('"', '').replace("'", '')
            
            # Verifica se o usuário quer sair
            if pdf_path.lower() == 'sair':
                print("Programa encerrado.")
                return
            
            # Se o usuário não digitou nada
            if not pdf_path:
                print("Por favor, digite um caminho de arquivo válido!")
                continue
            
            # Verifica se o arquivo existe
            if not os.path.exists(pdf_path):
                print(f"Erro: O arquivo '{pdf_path}' não foi encontrado.")
                retry = input("Deseja tentar novamente? (s/n): ").lower()
                if retry != 's' and retry != 'sim':
                    print("Programa encerrado.")
                    return
                continue
            
            # Processa o arquivo
            sucesso = processar_arquivo(pdf_path)
            
            # Pergunta se quer continuar apenas se o processamento foi bem sucedido
            if sucesso:
                retry = input("\nDeseja processar outro arquivo? (s/n): ").lower()
                if retry != 's' and retry != 'sim':
                    print("Programa encerrado.")
                    return
            else:
                retry = input("Deseja tentar novamente? (s/n): ").lower()
                if retry != 's' and retry != 'sim':
                    print("Programa encerrado.")
                    return
        
        except Exception as e:
            print(f"Erro inesperado: {str(e)}")
            retry = input("Deseja tentar novamente? (s/n): ").lower()
            if retry != 's' and retry != 'sim':
                print("Programa encerrado.")
                return

if __name__ == "__main__":
    main()
    