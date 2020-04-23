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
 * @property {string} question - The question that will be asked to the user.
 * @property {string} name - The name of the GET/POST parameter.
 * @property {boolean} required - Wether or not the input is required.
 */

/**
 * @typedef {BasicQuestion} Question 
 * A question of the survey. @extends BasicQuestion.
 * @property {string} [type] - The type of question.
 * @property {Object} [rules] - Various additional rules. Can be any HTML attribute accepted by the current input type.
 * @property {string} [placeholder] - The input placeholder.
 * @property {string[]} [choices] - A list of choices. Used only if type is 'choice'. 
 * @property {string|BasicQuestion[]} question - If it's a string, the same as BasicQuestion.question. If an array of BasicQuestion, a list of questions used if type is 'likert'.
 */

/**
 * @typedef {Object} Section
 * A section of the survey.
 * @property {string} [title] - The section's title.
 * @property {Question[]} questions - The section's questions.
 */

/**
 * @typedef {Object} Survey
 * The survey configuration object.
 * @property {string} introduction - The introduction to the survey. Treated as raw HTML.
 * @property {Section[]} sections - The survey's sections.
 */

/**
 * @type {Survey}
 */
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
            title: "Anagrafica",
            questions: [
                {
                    name: "age",
                    question: "Età",
                    type: "number",
                    rules: {
                        min: 0,
                        step: 1,
                    },
                    required: true,
                },
                {
                    name: "email",
                    question: "E-mail",
                    type: "email",
                    required: true,
                    placeholder: "youremail@email.com"
                },
                {
                    name: "sex",
                    question: "Sesso",
                    type: "choice",
                    required: true,
                    choices: [
                        "Maschio", "Femmina", "Altro"
                    ]
                }
            ]
        },
        {
            title: "Informazioni varie",
            questions: [
                {
                    question: [
                        {
                            name: "internet",
                            question: "Navigo su internet molto spesso",
                            required: true
                        },
                    ],
                    type: "likert",
                    required: true,
                }
            ]
        },
    ]
};
