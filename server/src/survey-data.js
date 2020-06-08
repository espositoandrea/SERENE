/*
 * The server component create for Andrea Esposito's Bachelor's Thesis.
 * Copyright (C) 2020  Andrea Esposito <a.esposito39@studenti.uniba.it>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

/**
 * @typedef {Object} BasicQuestion
 * A basic question of the survey. This class contains all the required field of a question.
 * 
 * @property {string} question - The question that will be asked to the user.
 * @property {string} name - The name of the GET/POST parameter.
 * @property {boolean} required - Wether or not the input is required.
 */

/**
 * @typedef {Object} ChoiceDescription
 * A description of a Question choice.
 * 
 * @property {string} label - The label of the choice. This will be seen by the user.
 * @property {any} value - The value of the choice. This will be sent to the server.
 */

/**
 * @typedef {BasicQuestion} Question 
 * A question of the survey. @extends BasicQuestion.
 * 
 * @property {string} [type] - The type of question.
 * @property {Object} [rules] - Various additional rules. Can be any HTML attribute accepted by the current input type.
 * @property {string} [placeholder] - The input placeholder.
 * @property {ChoiceDescription[]|number} [choices] - A list of choices. Used only if type is 'choice' or 'radios'. If it's a number n, it's used to generate n ChoiceDescription objects having {label: i, value: i}, con 1 <= i <= n.
 * @property {string|BasicQuestion[]} question - If it's a string, the same as BasicQuestion.question. If an array of BasicQuestion, a list of questions used if type is 'likert'.
 */

/**
 * @typedef {Object} Section
 * A section of the survey.
 * 
 * @property {string} [title] - The section's title.
 * @property {Question[]} questions - The section's questions.
 */

/**
 * @typedef {Object} Survey
 * The survey configuration object.
 * 
 * @property {string} introduction - The introduction to the survey. Treated as raw HTML.
 * @property {Section[]} sections - The survey's sections.
 */

/**
 * @type {Survey}
 */
module.exports = {
    introdution: `
        <p>Ti ringraziamo per preso parte a questa raccolta dati.</p>
        <p>
            Ti ricordiamo che tutto il processo di raccolta dati è completamento
            anonimo. Infatti, le immagini che saranno catturate dalla webcam saranno:
            <ol>
                <li>Inviate al nostro server utilizzando una connessione cifrata</li>
                <li>Elaborate istantaneamente per ricavare le emozioni dalle espressioni
                    facciali</li>
                <li>Immediatamente cancellate in maniera permanente</li>
            </ol>
        </p>
        <p>
            Per una maggiore trasparenza mettiamo a disposizione il codice sorgente
            dell'intero progetto dal quale si può avere conferma dei meccanismi
            precedentemente citati a garanzia del completo anonimato. Il codice sorgente
            è pubblicato su
            <a href="https://github.com/espositoandrea/Bachelor-Thesis" target="_blank"
               rel="noopener noreferrer">
                <span class="fab fa-github" aria-hidden="true"></span> GitHub</a>.
        </p>
        <p>
            Inoltre, per una maggiore garanzia, tutti i dati raccolti sono disponibili
            alla consultazione al seguente indirizzo: <a
            href="http://giuseppe-desolda.ddns.net:10001/" target="_blank" rel="noopener
            noreferrer">giuseppe-desolda.ddns.net:10001</a>
        </p>
    `,
    sections: [
        {
            title: "Anagrafica",
            questions: [
                {
                    name: "age",
                    question: "Età",
                    type: "choice",
                    required: true,
                    choices: [
                        {
                            label: "Inferiore ai 18 anni",
                            value: 0
                        },
                        {
                            label: "Tra i 18 e i 29 (inclusi)",
                            value: 1
                        },
                        {
                            label: "Tra i 30 e i 39 (inclusi)",
                            value: 2
                        },
                        {
                            label: "Tra i 40 e i 49 (inclusi)",
                            value: 3
                        },
                        {
                            label: "Tra i 50 e i 59 (inclusi)",
                            value: 4
                        },
                        {
                            label: "Oltre i 60",
                            value: 5
                        },
                    ],
                },
                {
                    name: "gender",
                    question: "Genere",
                    type: "choice",
                    required: true,
                    choices: [
                        {
                            label: "Maschio",
                            value: "m"
                        },
                        {
                            label: "Femmina",
                            value: "f"
                        },
                        {
                            label: "Altro",
                            value: "a"
                        }
                    ]
                },
                {
                    name: "internet",
                    question: "Quanto ore usi mediamente internet ogni giorno?",
                    type: "radios",
                    choices: 24,
                    required: true,
                }
            ]
        },
    ]
};
