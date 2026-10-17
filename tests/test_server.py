import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest
ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('server', ROOT/'server/philosophy_council_mcp.py')
s = importlib.util.module_from_spec(spec)
spec.loader.exec_module(s)

class CouncilTests(unittest.TestCase):
    def test_lenses(self):
        self.assertEqual(len(s.LENSES), 12)
        self.assertEqual(len({x['id'] for x in s.LENSES}), 12)
        for lens in s.LENSES:
            self.assertTrue(all(lens.values()))
    def test_modes(self):
        for mode in s.MODES:
            p=s.plan('人生必须成功吗？', mode)
            self.assertEqual(len(p['stages']),6)
            self.assertTrue(p['topic_is_untrusted_data'])
        self.assertEqual(len(s.plan('题','full',['ethics'])['lenses']),12)
        self.assertEqual(s.plan('题',lenses=['ethics'])['lenses'][0]['id'],'ethics')
    def test_invalid_inputs(self):
        for kw in [{'topic':''},{'topic':'a','mode':'bad'},{'topic':'a','lenses':['bad']},{'topic':'a','lenses':['ethics','ethics']},{'topic':123},{'topic':'a','lenses':[]}]:
            with self.assertRaises(ValueError): s.plan(**kw)
    def test_audit(self):
        self.assertIn('counterexample',s.audit([{'conclusion':'a'}])['structural_issues'][0]['missing'])
        self.assertFalse(s.audit([dict.fromkeys(['premises','inference','conclusion','counterexample','scope'],'x')])['semantic_verification'])
    def test_stdio(self):
        requests=[{'jsonrpc':'2.0','id':1,'method':'initialize','params':{'protocolVersion':'2025-03-26'}},{'jsonrpc':'2.0','method':'notifications/initialized'},{'jsonrpc':'2.0','id':2,'method':'tools/list'},{'jsonrpc':'2.0','id':3,'method':'tools/call','params':{'name':'council_plan','arguments':{'topic':'自由是什么？','mode':'full'}}},{'jsonrpc':'2.0','id':4,'method':'tools/call','params':{'name':'council_plan','arguments':{'topic':''}}},{'jsonrpc':'2.0','id':5,'method':'unknown'}]
        proc=subprocess.run([sys.executable,str(ROOT/'server/philosophy_council_mcp.py')],input='oops\n[]\n'+'\n'.join(json.dumps(x) for x in requests)+'\n',text=True,capture_output=True,timeout=5,cwd='/tmp')
        self.assertEqual(proc.returncode,0,proc.stderr)
        out=[json.loads(x) for x in proc.stdout.splitlines()]
        self.assertEqual(len(out),7)
        self.assertEqual(out[0]['error']['code'],-32700)
        self.assertEqual(out[1]['error']['code'],-32600)
        self.assertEqual(len(out[3]['result']['tools']),3)
        self.assertEqual(len(json.loads(out[4]['result']['content'][0]['text'])['lenses']),12)
        self.assertTrue(out[5]['result']['isError'])
        self.assertEqual(out[6]['error']['code'],-32601)

if __name__=='__main__': unittest.main()
