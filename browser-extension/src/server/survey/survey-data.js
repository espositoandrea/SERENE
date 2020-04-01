module.exports = {
    introdution: `<p>Lorem ipsum dolor sit amet consectetur adipisicing elit.
                    Explicabo porro beatae dolorem magni a quaerat quia cum deleniti
                    doloremque reiciendis ut in recusandae itaque repellat, quos harum
                    incidunt qui! Facere.</p>
                <p>Lorem ipsum dolor sit amet consectetur adipisicing elit.
                    Excepturi neque voluptas, alias deleniti pariatur facilis reiciendis
                    asperiores eum? Atque, ratione laboriosam. Repellat, saepe!
                    Inventore ab, dolore vitae recusandae natus amet!</p>`,
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
                },
                {
                    name: 'sex',
                    question: 'Sesso',
                    type: 'choice',
                    required: true,
                    choices: [
                        'Maschio', 'Femmina', 'Altro'
                    ]
                }
            ]
        },
        {
            title: "Informazioni varie",
            questions: [
                {
                    name: 'internet',
                    question: 'Navigo su internet molto spesso',
                    type: 'likert',
                    required: true,
                }
            ]
        },
    ]
};
