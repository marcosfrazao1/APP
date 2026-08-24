# Monitoramento de Efluente de ETE

MVP para monitoramento em tempo real da qualidade do efluente tratado na saída de uma estação de tratamento de esgoto (ETE).

## Arquitetura

`Sensores -> ESP32 -> API -> Banco de dados -> Dashboard Web/Mobile`

O MVP foi desenhado para uma única câmara de monitoramento na saída da ETE. A câmara fica acessível e os elementos sensores ficam em contato com o efluente; a eletrônica permanece protegida e seca.

## Parâmetros

- pH
- Turbidez
- Condutividade elétrica
- Temperatura
- Oxigênio dissolvido
- Vazão (opcional no hardware inicial)

## Princípios científicos

- Os valores do protótipo são dados de monitoramento e não substituem análises laboratoriais.
- O sistema deve guardar a leitura bruta, timestamp, estado de comunicação e versão de calibração.
- Alertas são alertas de monitoramento; não classificam automaticamente conformidade ou irregularidade.
- A validação será feita comparando leituras do sistema com métodos/equipamentos de referência.

## Estrutura

- `firmware/` — firmware inicial do ESP32.
- `backend/` — API de ingestão e consulta de leituras.
- `dashboard/` — painel responsivo para web e celular.

## Próximos passos de hardware

1. Confirmar modelos e interfaces dos sensores.
2. Montar e testar a câmara de passagem.
3. Calibrar cada sensor.
4. Implementar leitura real no firmware.
5. Validar contra laboratório/equipamento de referência.
6. Só então instalar em ponto autorizado de uma ETE.
