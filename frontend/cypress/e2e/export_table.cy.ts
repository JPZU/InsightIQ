describe('Table Export Feature', () => {
  beforeEach(() => {
    // Visita la vista principal de chat
    cy.visit('http://localhost:5173/chat')
  })

  it('successfully exports table to CSV', () => {
    // Simula una consulta válida que devuelva una tabla
    cy.get('input[placeholder="Type here..."]').type('Show me the amount of women and men')
    cy.intercept('POST', '**/api/chat', {
      statusCode: 200,
      body: {
        response: {
          input: 'Show me the amount of women and men',
          output: 'There are 300 women and 500 men.',
          query: 'SELECT gender, COUNT(*) FROM users GROUP BY gender',
          query_output: [
            ['Female', 300],
            ['Male', 500],
          ],
          x_axis: ['Female', 'Male'],
          y_axis: [300, 500],
        },
      },
    }).as('chatRequest')
    cy.contains('Send').click()
    // Cambia a vista de tabla
    cy.contains('Table').click()
    cy.get('table').should('exist') // waits for the table to render
    cy.get('table tbody tr').should('have.length.greaterThan', 0) // ensure rows are loaded
    
    // Selecciona CSV
    cy.get('select').select('csv')

    // Haz clic en el botón de descarga
    cy.contains('Download Table').click()

    // Verifica que el mensaje de éxito aparezca
    cy.contains('CSV file downloaded successfully!').should('be.visible')
  })

  it('successfully exports table to XLSX', () => {
    // Simula una consulta válida que devuelva una tabla
    cy.get('input[placeholder="Type here..."]').type('Show me the amount of women and men')
    cy.intercept('POST', '**/api/chat', {
      statusCode: 200,
      body: {
        response: {
          input: 'Show me the amount of women and men',
          output: 'There are 300 women and 500 men.',
          query: 'SELECT gender, COUNT(*) FROM users GROUP BY gender',
          query_output: [
            ['Female', 300],
            ['Male', 500],
          ],
          x_axis: ['Female', 'Male'],
          y_axis: [300, 500],
        },
      },
    }).as('chatRequest')
    cy.contains('Send').click()

    // Cambia a vista de tabla
    cy.contains('Table').click()

    // Espera que la tabla se muestre
    cy.get('table').should('exist')

    // Selecciona XLSX
    cy.get('select').select('xlsx')

    // Haz clic en el botón de descarga
    cy.contains('Download Table').click()

    // Verifica que el mensaje de éxito aparezca
    cy.contains('XLSX file downloaded successfully!').should('be.visible')
  })

  it('shows error message when no data is available', () => {
    
    // Simula una consulta válida que devuelva una tabla
    cy.get('input[placeholder="Type here..."]').type('Show me the amount of women and men')

    cy.contains('Send').click()
    
    // Cambia a vista de tabla antes de enviar la pregunta
    cy.contains('Table').click()

    // Verifica el mensaje de error
    cy.contains('Table not available. No valid data to display.').should('be.visible')
  })
})
