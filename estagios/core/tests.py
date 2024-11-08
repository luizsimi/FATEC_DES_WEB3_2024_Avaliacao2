from django.test import TestCase
from django.shortcuts import resolve_url as r
from core.models import VagaModel
from core.forms import VagaForm
from django.db.models.query import QuerySet


class Index_GET_POST_Test(TestCase):
    def setUp(self):
        self.resp = self.client.get(r('core:index'), follow=True)
        self.resp_post = self.client.post(r('core:index'))

    def test_status_code(self):
        self.assertEqual(self.resp.status_code , 200)
        self.assertEqual(self.resp_post.status_code , 302)
    
    def test_template_used(self):
        self.assertTemplateUsed(self.resp, 'index.html')

    def test_found_html(self):
        tags = (
            ('<html', 1),
            ('<body>', 1),
            ('Vagas de Estágio', 3),
            ('<input', 4),
            ('<br>', 5),
            ('</body>', 1),
            ('</html>', 1),
        )
        for text, count in tags:
            with self.subTest():
                self.assertContains(self.resp, text, count)


class VagaModelTest(TestCase):
    def setUp(self):
        VagaModel.objects.create(
            titulo='Suporte Júnior',
            empresa='Google',
            telefone='9999999999',
            email='junior@suporte.com',
            descritivo='vaga para todos os junior')
        self.vaga = VagaModel.objects.first()

    def test_str(self):
        self.assertEqual(str(self.vaga), 'Suporte Júnior')

    def test_created(self):
        self.assertTrue(VagaModel.objects.exists())

    def test_data_saved(self):
        data = VagaModel.objects.first()
        self.assertEqual(data.titulo, 'Suporte Júnior')
        self.assertEqual(data.empresa, 'Google')
        self.assertEqual(data.telefone, '9999999999')
        self.assertEqual(data.email, 'junior@suporte.com')
        self.assertEqual(data.descritivo, 'vaga para todos os junior')


class VagaFormTest(TestCase):
    def test_unbounded_fields(self):
        form = VagaForm()
        expected = ['titulo','empresa', 'telefone', 'descritivo' , 'email']
        self.assertSequenceEqual(expected, list(form.fields))

    def test_form_all_OK(self):
        dados = dict(titulo='Suporte Júnior', empresa='Google', telefone='1999998888', email='suporte@junior.com', descritivo='vaga para junior')
        form = VagaForm(dados)
        errors = form.errors
        self.assertEqual({}, errors)
        self.assertEqual(form.cleaned_data['titulo'], 'SUPORTE JÚNIOR')

    def test_form_wrong_DDD(self):
        dados = dict(titulo='Suporte Júnior', empresa='Google', telefone='9999998888', email='suportejunior@gmail.com', descritivo='vaga para junior')
        form = VagaForm(dados)
        errors = form.errors
        errors_list = errors['telefone']
        msg = 'DDD válido somente o 19'
        self.assertEqual([msg], errors_list)

    def test_form_wrong_companyName(self):
        dados = dict(titulo='Suporte Júnior', empresa='X', telefone='9999998888', email='suportecasa@gmail.com', descritivo='vaga para assessor')
        form = VagaForm(dados)
        errors = form.errors
        errors_list = errors['empresa']
        msg = 'Empresa precisa ter ao menos dois caracteres'
        self.assertEqual([msg], errors_list)

    def test_form_fail_1(self):
        dados = dict(telefone='1999998888')
        form = VagaForm(dados)
        errors = form.errors
        errors_list = errors['titulo']
        msg = 'This field is required.'
        self.assertEqual([msg], errors_list)
    
    def test_form_fail_2(self):
        dados = dict(nome='José da Silva')
        form = VagaForm(dados)
        errors = form.errors
        errors_list = errors['telefone']
        msg = 'This field is required.'
        self.assertEqual([msg], errors_list)

    def test_form_fail_3(self):
        dados = dict(email='suportejunior@gmail.com')
        form = VagaForm(dados)
        errors = form.errors
        errors_list = errors['descritivo']
        msg = 'This field is required.'
        self.assertEqual([msg], errors_list)
    
    def test_form_fail_4(self):
        dados = dict(descritivo='vaga para developer')
        form = VagaForm(dados)
        errors = form.errors
        errors_list = errors['email']
        msg = 'This field is required.'
        self.assertEqual([msg], errors_list)


class Create_GET_Test(TestCase):
    def setUp(self):
        self.resp = self.client.get(r('core:create'), follow=True)

    def test_status_code(self):
        self.assertEqual(self.resp.status_code , 200)
  
    def test_context(self):
        form_used = self.resp.context['form']
        self.assertIsInstance(form_used, VagaForm)
          
    def test_template_used(self):
        self.assertTemplateUsed(self.resp, 'cadastro.html')


class Create_POST_OK_Test(TestCase):
    def setUp(self):
        data = {'titulo': 'Suporte Júnior',
                'empresa': 'Google',
                'telefone': '19-98888-7777',
                'email': 'suporte@junior.com',
                'descritivo': 'vaga para desenvolvedor'}
        self.resp = self.client.post(r('core:create'), data, follow=True)
        self.resp2 = self.client.post(r('core:create'), data)

    def test_status_code(self):
        self.assertEqual(self.resp.status_code , 200)
        self.assertEqual(self.resp2.status_code , 302)
  
    def test_template_used(self):
        self.assertTemplateUsed(self.resp, 'index.html')


class Create_POST_Fail_Test(TestCase):
    def setUp(self):
        data = {'titulo': 'Suporte Júnior',
                'empresa': 'XP',
                'telefone': '9988887777',
                'email' : 'suport@xpinveste.com',
                'descritivo': 'vaga para CEO'}
        self.resp = self.client.post(r('core:create'), data, follow=True)
        self.resp2 = self.client.post(r('core:create'), data)

    def test_status_code(self):
        self.assertEqual(self.resp.status_code , 200)
        self.assertEqual(self.resp2.status_code , 200)
  
    def test_context(self):
        form_used = self.resp.context['form']
        self.assertIsInstance(form_used, VagaForm)
          
    def test_template_used(self):
        self.assertTemplateUsed(self.resp, 'cadastro.html')


class Read_GET_Test(TestCase):
    def setUp(self):
        self.resp = self.client.get(r('core:read'), follow=True)

    def test_status_code(self):
        self.assertEqual(self.resp.status_code , 200)
  
    def test_context(self):
        form_used = self.resp.context['vagas']
        self.assertIsInstance(form_used, QuerySet)
          
    def test_template_used(self):
        self.assertTemplateUsed(self.resp, 'listar.html')


class Read_POST_OK_Test(TestCase):
    def setUp(self):
        data = {'titulo': 'Suporte Júnior',
                'empresa': 'Google',
                'telefone': '19-98888-7777',
                'email': 'suporte@junior.com',
                'descritivo' : 'vaga para junior'}
        VagaModel.objects.create(**data)
        data = {'id':1}
        self.resp = self.client.post(r('core:read'), data, follow=True)
        self.resp2 = self.client.post(r('core:read'), data)

    def test_status_code(self):
        self.assertEqual(self.resp.status_code , 200)
        self.assertEqual(self.resp2.status_code , 200)
  
    def test_template_used(self):
        self.assertTemplateUsed(self.resp, 'detalhes.html')

    def test_found_html(self):
        tags = (
            ('<html', 1),
            ('<body>', 1),
            ('Cadastro de Vagas de Estágio', 1),
            ('Vagas de Estágio', 3),
            ('Suporte Júnior', 1),
            ('Google', 1),
            ('</body>', 1),
            ('</html>', 1),
        )
        for text, count in tags:
            with self.subTest():
                self.assertContains(self.resp, text, count)


class Read_POST_Fail_Test(TestCase):
    def setUp(self):
        data = {'titulo': 'Suporte Júnior',
                'telefone': '19-98888-7777',}
        VagaModel.objects.create(**data)
        data = {}
        self.resp = self.client.post(r('core:read'), data, follow=True)
        self.resp2 = self.client.post(r('core:read'), data)

    def test_status_code(self):
        self.assertEqual(self.resp.status_code , 200)
        self.assertEqual(self.resp2.status_code , 200)
  
    def test_template_used(self):
        self.assertTemplateUsed(self.resp, 'detalhes.html')

    def test_found_html(self):
        tags = (
            ('<html', 1),
            ('<body>', 1),
            ('Cadastro de Vagas de Estágio', 1),
            ('Vagas de Estágio', 3),
            ('Nenhuma vaga cadastrada', 1),
            ('</body>', 1),
            ('</html>', 1),
        )
        for text, count in tags:
            with self.subTest():
                self.assertContains(self.resp, text, count)
    

class Update_GET_Test(TestCase):
    def setUp(self):
        self.resp = self.client.get(r('core:update'), follow=True)

    def test_status_code(self):
        self.assertEqual(self.resp.status_code , 200)
  
    def test_context(self):
        form_used = self.resp.context['vagas']
        self.assertIsInstance(form_used, QuerySet)
          
    def test_template_used(self):
        self.assertTemplateUsed(self.resp, 'atualizar.html')


class Update_POST_OK_Test(TestCase):
    def setUp(self):
        data = {'titulo': 'Suporte Júnior',
                'empresa': 'Google',
                'telefone': '19-98888-7777',
                'email' : 'junior@gmail.com',
                'descritivo' : 'vaga para todos os desenvolvedores'}
        VagaModel.objects.create(**data)
        data = {'id':1}
        self.resp = self.client.post(r('core:update'), data, follow=True)
        self.resp2 = self.client.post(r('core:update'), data)

    def test_status_code(self):
        self.assertEqual(self.resp.status_code , 200)
        self.assertEqual(self.resp2.status_code , 200)
  
    def test_template_used(self):
        self.assertTemplateUsed(self.resp, 'atualizar2.html')

    def test_found_html(self):
        tags = (
            ('<html', 1),
            ('<body>', 1),
            ('Vagas de Estágio', 3),
            ('Suporte Júnior', 1),
            ('</body>', 1),
            ('</html>', 1),
        )
        for text, count in tags:
            with self.subTest():
                self.assertContains(self.resp, text, count)


class Update_POST_Fail_Test(TestCase):
    def setUp(self):
        data = {'titulo': 'Suporte Júnior',
                'empresa': 'Google',
                'telefone': '19-98888-7777',}
        VagaModel.objects.create(**data)
        data = {}
        self.resp = self.client.post(r('core:update'), data, follow=True)
        self.resp2 = self.client.post(r('core:update'), data)

    def test_status_code(self):
        self.assertEqual(self.resp.status_code , 200)
        self.assertEqual(self.resp2.status_code , 200)
  
    def test_template_used(self):
        self.assertTemplateUsed(self.resp, 'atualizar2.html')

    def test_found_html(self):
        tags = (
            ('<html', 1),
            ('<body>', 1),
            ('Vagas de Estágio', 3),
            ('Nenhuma vaga cadastrada', 1),
            ('</body>', 1),
            ('</html>', 1),
        )
        for text, count in tags:
            with self.subTest():
                self.assertContains(self.resp, text, count)


class Confirm_Update_GET_Test(TestCase):
    def setUp(self):
        self.resp = self.client.get(r('core:confirm_update'), follow=True)

    def test_status_code(self):
        self.assertEqual(self.resp.status_code , 200)
          
    def test_template_used(self):
        self.assertTemplateUsed(self.resp, 'index.html')


class Confirm_Update_POST_OK_Test(TestCase):
    def setUp(self):
        data = {'titulo': 'Suporte Júnior',
                'empresa': 'Google',
                'telefone': '19-98888-7777',
                'email' : 'suportejunior@gmail.com',
                'descritivo' : 'desenvolvedor Senior'}
        VagaModel.objects.create(**data)
        data = {'titulo': 'Suporte Sênior',
                'empresa': 'Google Inc',
                'telefone': '19-98888-9999',
                'email' : 'suportevss@gmail.com',
                'descritivo' : 'vaga para todos',
                'id':1}
        self.resp = self.client.post(r('core:confirm_update'), data, follow=True)
        self.resp2 = self.client.post(r('core:confirm_update'), data)

    def test_status_code(self):
        self.assertEqual(self.resp.status_code , 200)
        self.assertEqual(self.resp2.status_code , 200)
  
    def test_template_used(self):
        self.assertTemplateUsed(self.resp, 'atualizar.html')
    
    def test_data_changed(self):
        instance = VagaModel.objects.first()
        self.assertEqual(instance.titulo, 'SUPORTE SÊNIOR')
        self.assertEqual(instance.telefone, '19-98888-9999')


class Confirm_Update_POST_Fail_Test(TestCase):
    def setUp(self):
        data = {'titulo': 'Suporte Júnior',
                'empresa': 'Google',
                'telefone': '19-98888-7777',
                'descritivo' : 'error'}
        VagaModel.objects.create(**data)
        data = {'telefone': '19-98888-7777','id':1}
        self.resp = self.client.post(r('core:confirm_update'), data, follow=True)
        self.resp2 = self.client.post(r('core:confirm_update'), data)

    def test_status_code(self):
        self.assertEqual(self.resp.status_code , 200)
        self.assertEqual(self.resp2.status_code , 200)
  
    def test_template_used(self):
        self.assertTemplateUsed(self.resp, 'atualizar2.html')
    
    def test_data_not_changed(self):
        instance = VagaModel.objects.first()
        self.assertEqual(instance.titulo, 'Suporte Júnior')
        self.assertEqual(instance.telefone, '19-98888-7777')



class Delete_GET_Test(TestCase):
    def setUp(self):
        self.resp = self.client.get(r('core:delete'), follow=True)

    def test_status_code(self):
        self.assertEqual(self.resp.status_code , 200)
          
    def test_template_used(self):
        self.assertTemplateUsed(self.resp, 'remover.html')


class Delete_POST_OK_Test(TestCase):
    def setUp(self):
        data = {'titulo': 'Suporte Júnior',
                'empresa': 'Google',
                'telefone': '19-98888-7777',
                'email' : 'suportegoogle@gmail.com',
                'descritivo' : 'vaga para todos'}
        VagaModel.objects.create(**data)
        data = {'id':1}
        self.resp = self.client.post(r('core:delete'), data, follow=True)

    def test_status_code(self):
        self.assertEqual(self.resp.status_code , 200)
  
    def test_template_used(self):
        self.assertTemplateUsed(self.resp, 'index.html')
    
    def test_deleted(self):
        self.assertFalse(VagaModel.objects.exists())

class Delete_POST_Fail_Test(TestCase):
    def setUp(self):
        data = {'titulo': 'Suporte Júnior',
                'empresa': 'Google',
                'telefone': '19-98888-7777',
                'email' : 'suporte@gmail.com',
                'descritivo' : 'vaga para fatec'}
        VagaModel.objects.create(**data)
        data = {'id':2}
        self.resp = self.client.post(r('core:delete'), data, follow=True)

    def test_status_code(self):
        self.assertEqual(self.resp.status_code , 200)
  
    def test_template_used(self):
        self.assertTemplateUsed(self.resp, 'index.html')
    
    def test_not_deleted(self):
        self.assertTrue(VagaModel.objects.exists())
