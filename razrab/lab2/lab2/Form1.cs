namespace lab2
{
    public partial class Form1 : Form
    {
        List<User> users;
        public Form1()
        {
            users = new List<User>();
            InitializeComponent();
        }
        private void button1_Click(object sender,EventArgs e)
        {
            string text = " ";
            text += "����";
            text += textBox1.Text + "\n";
            text += "�����: ";
            text += listBox1.Text + "\n";
            if (radioButton1.Checked) text += "����������\n";
            if (radioButton2.Checked) text += "�� ����������\n";
            for(int i=0;i<checkedListBox1.ChekedItems.Count;i++)
            {
                text+=checked
            }
        }
    }

}