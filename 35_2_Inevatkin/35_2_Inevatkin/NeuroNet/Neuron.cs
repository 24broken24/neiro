using System;
using static System.Math;

namespace _35_2_Inevatkin.NeuroNet
{
    class Neuron
    {
        private NeuronType type;  // Тип нейрона
        private double[] _weights;
        private double[] _inputs;
        private double _output;
        private double _derivative; // Производная функции активации
        private double a = 0.01; // Константа для функции активации (не используется с Tanh, но оставлю для других случаев)

        public double[] Weights { get => _weights; set => _weights = value; }
        public double[] Inputs { get => _inputs; set => _inputs = value; }
        public double Output { get => _output; }
        public double Derivative { get => _derivative; }

        // Конструктор класса
        public Neuron(double[] weigths, NeuronType type)
        {
            this.type = type;
            _weights = weigths;
        }

        // Метод активации нейрона гиперболический тангенс 
        public void Activator(double[] inputs, double[] w)
        {
            _inputs = inputs;
            double sum = w[0];  // Начальная сумма (включая смещение)

            // Вычисляем сумму входных значений, умноженных на соответствующие веса
            for (int m = 0; m < _inputs.Length; m++)
            {
                sum += _inputs[m] * _weights[m + 1];
            }

            // Определяем функцию активации для скрытых и выходных нейронов
            switch (type)
            {
                case NeuronType.Hidden:
                    // Используем гиперболический тангенс для скрытого слоя
                    _output = Tanh(sum);
                    _derivative = 1 - _output * _output;  // Производная гиперболического тангенса
                    break;

                case NeuronType.Output:
                    // Для выходного нейрона можно использовать экспоненциальную функцию
                    _output = Exp(sum);
                    break;
            }
        }
    }
}
