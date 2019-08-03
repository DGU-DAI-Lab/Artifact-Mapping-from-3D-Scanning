## 1\. 용어 변경

지금까지 D-Seg.를 수행하여 얻은 3가지 영역에 대해 명칭을 어떻게 정해야 할지 몰라서 가칭(front, slice, behind)을 사용하고 있었다.

이에 따른 문제가 있었는데, slice는 python 내장 함수 slice()와 동일한 시그니쳐를 가지기에... 조금 찝찝했다.

보다 적합한 표현을 찾기위해 건축용어에 대한 구글링을 하던 중, 괜찮다고 생각한 용어 몇 가지를 골라보았다.

-   front (view / elevation) : 정면도
-   rear (view / elevation) : 배면도 (기존의 behind)
-   section : 단면 (기존의 slice)
-   cutting : 절단면
-   breakage : 파단면 

참고한 주소는 다음과 같다 :

1.  [https://m.blog.naver.com/chokwangshik/70105609713](https://m.blog.naver.com/chokwangshik/70105609713)
2.  [http://www.gunnet.kr/service/data/word-dwg.htm](http://www.gunnet.kr/service/data/word-dwg.htm)

## 2\. Section : Breakage / Cutting

지난 글 ([https://hepheir.tistory.com/135](https://hepheir.tistory.com/135))에서 제안한 방법을 이용하여 전면,배면,단면을 분리 할 경우 생기는 현상이 2가지 있다.

1.  section/front/rear 영역에 중복된 facet이 배치된다. --> 추후에 처리가 복잡해질 가능성이 있다.
2.  단면에 걸친 facet은 별다른 처리 없이 통채로 section/front/rear에 append 되었다.

1번 현상의 경우, 언급한 바와 같이 추후 처리에 영향을 미칠 수 있으므로, 중복을 없에기 위해, section 영역으로 분리된 facet은 front/rear로 분류되지 않도록 하였다.

### Breakage / Cutting

\*breakage / cutting 이라는 용어는 건축용어 중 '절단면(cutting)'과 '파단면(breakage)'에서 영감을 얻어 사용하였다.

-   절단면 (cutting)은 깔끔하게 잘린 단면을 의미한다.
-   파단면 (breaking)은 지저분하게 잘린 단면을 의미한다.

#### breakage

2번 현상의 경우, 단면에 걸친 facet이 단면에 딱 맞추어 깔끔하게 절단된 영역으로 나뉘지 않고, 해당 facet 전체가 section/front/rear로 들어가기에, D-segmentation이 끝나고 결과를 보면 section/front/rear각 영역의 가장자리를 이루는 모서리가 울퉁불퉁하게 나타나게된다.

이를 지저분하게 잘린 단면과 같다하여, breakage 과정이라고 하자.

```
def DepthSegmentation(obj):
    assert isinstance(obj,mesh.Mesh)

    print('D-Segmentation start.')
    start = time.time()

    ret = _breakage(obj)
    ret = _cutting(ret)

    end = time.time()
    print('D-Segmentation done.')
    print('total %d'%obj.__len__())
    print('took %f seconds'%(end-start))
    return np.array(ret)

def _breakage(obj):
    """메쉬를 전면, 측면, 단면으로 분류. 각 영역은 중복되지 않음."""
    z = obj.z
    n = obj.normals
    ret = [ [], [], [] ]
    for i in range(obj.__len__()):
        # Front or behind the xy-surface
        isFront = isBehind = False
        for _z in z[i]:
            isFront  |= (_z >= 0)
            isBehind |= (_z <= 0)

        #  - Find slices
        if isFront and isBehind:
            ret[1].append(obj.data[i])
        #  - Find fronts and behinds
        elif n[i,2] > 0:
            if isFront:
                ret[0].append(obj.data[i])
            if isBehind:
                ret[2].append(obj.data[i])
    return ret

def _cutting(obj):
    pass
```

(P.S. 측정해본 결과, 약 228만개의 facet을 가지는 고배1.stl의 breakage과정에는 대략 37~38초가 소요되었다.)