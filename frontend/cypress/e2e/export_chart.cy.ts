describe('Chart Download Export E2E', () => {
    beforeEach(() => {
      cy.visit('http://localhost:5173/chat')
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
    })
  
    it('should display chart and allow downloading as PNG', () => {
      // Step 1: Send a valid question
      cy.get('input[placeholder="Type here..."]').type('Show me the amount of women and men')
      cy.contains('Send').click()
  
      // Step 2: Wait for intercepted response
      cy.wait('@chatRequest', { timeout: 10000 }).its('response.statusCode').should('eq', 200)
  
      // Step 3: Switch to chart view
      cy.contains('Charts').click()
  
      // Step 4: Wait for chart dropdown to appear
      cy.get('select#chart-type').should('be.visible')
  
      // Step 5: Select export format
      cy.get('select').eq(1).select('png') // selector for export format dropdown
      cy.contains('Download Chart').click()
  
      // Step 6: Confirm feedback message appears
      cy.contains('Chart downloaded as PNG.').should('exist')
    })

    it('should display chart and allow downloading as PDF', () => {
        // Step 1: Send a valid question
        cy.get('input[placeholder="Type here..."]').type('Show me the amount of women and men')
        cy.contains('Send').click()
    
        // Step 2: Wait for intercepted response
        cy.wait('@chatRequest', { timeout: 10000 }).its('response.statusCode').should('eq', 200)
    
        // Step 3: Switch to chart view
        cy.contains('Charts').click()
    
        // Step 4: Wait for chart dropdown to appear
        cy.get('select#chart-type').should('be.visible')
    
        // Step 5: Select export format
        cy.get('select').eq(1).select('pdf') // selector for export format dropdown
        cy.contains('Download Chart').click()
    
        // Step 6: Confirm feedback message appears
        cy.contains('Chart downloaded as PDF.').should('exist')
      })

    it('should display chart and allow downloading as PNG', () => {
        // Step 1: Send a valid question
        cy.get('input[placeholder="Type here..."]').type('Show me the amount of women and men')
        cy.contains('Send').click()
    
        // Step 2: Wait for intercepted response
        cy.wait('@chatRequest', { timeout: 10000 }).its('response.statusCode').should('eq', 200)
    
        // Step 3: Switch to chart view
        cy.contains('Charts').click()
    
        // Step 4: Wait for chart dropdown to appear
        cy.get('select#chart-type').should('be.visible')
    
        // Step 5: Select export format
        cy.get('select').eq(1).select('png') // selector for export format dropdown
        cy.contains('Download Chart').click()
    
        // Step 6: Confirm feedback message appears
        cy.contains('Chart downloaded as PNG.').should('exist')
      })
  })
  