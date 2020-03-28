module.exports = {
    sections: [
        {
            title: 'Anagrafica',
            questions: [
                {
                    name: 'name',
                    question: 'Nome',
                    type: 'text',
                    required: true,
                },
                {
                    name: 'surname',
                    question: 'Cognome',
                    type: 'text',
                    required: true,
                },
                {
                    name: 'age',
                    question: 'Età',
                    type: 'number',
                    rules: {
                        min: 0,
                        step: 1,
                    },
                    required: true,
                },
                {
                    name: 'email',
                    question: 'E-mail',
                    type: 'email',
                    required: true,
                    placeholder: 'youremail@email.com'
                }
            ]
        },
    ]
};