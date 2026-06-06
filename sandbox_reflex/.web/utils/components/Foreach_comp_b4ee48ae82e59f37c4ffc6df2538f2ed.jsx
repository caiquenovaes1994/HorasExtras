
import {Fragment,memo,useContext,useEffect} from "react"
import {ReflexEvent,applyEventActions,isTrue} from "$/utils/state"
import {EventLoopContext,StateContexts} from "$/utils/context"
import {Button as RadixThemesButton,Flex as RadixThemesFlex,Table as RadixThemesTable,Text as RadixThemesText,Tooltip as RadixThemesTooltip} from "@radix-ui/themes"
import {TriangleAlert as LucideTriangleAlert} from "lucide-react"
import {jsx} from "@emotion/react"






export const Foreach_comp_b4ee48ae82e59f37c4ffc6df2538f2ed = memo(({children}) => {
    const reflex___state____state__sandbox_reflex___state_hoteis____hotel_state = useContext(StateContexts.reflex___state____state__sandbox_reflex___state_hoteis____hotel_state)
const [addEvents, connectErrors] = useContext(EventLoopContext);



    return(
        Array.prototype.map.call(reflex___state____state__sandbox_reflex___state_hoteis____hotel_state.filtered_hoteis_rx_state_ ?? [],((h_rx_state_,index_cfacad231ec0a393aca12f812146566a)=>(jsx(RadixThemesTable.Row,{key:index_cfacad231ec0a393aca12f812146566a},jsx(RadixThemesTable.Cell,{},jsx(RadixThemesText,{as:"p",weight:"bold"},h_rx_state_?.["rid"])),jsx(RadixThemesTable.Cell,{},h_rx_state_?.["nome"]),jsx(RadixThemesTable.Cell,{align:"center"},jsx(Fragment,{},(isTrue(h_rx_state_?.["has_pendency"])?(jsx(Fragment,{},jsx(RadixThemesTooltip,{content:(h_rx_state_?.["pendencia_tipo"]+" Pendente")},jsx(LucideTriangleAlert,{css:({ ["color"] : "#f39c12" }),size:20},)))):(jsx(Fragment,{},jsx(RadixThemesText,{as:"p",css:({ ["color"] : "#666" })},"-")))))),jsx(RadixThemesTable.Cell,{align:"right"},jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",direction:"row",justify:"end",gap:"2"},jsx(RadixThemesButton,{css:({ ["cursor"] : "pointer" }),disabled:h_rx_state_?.["has_pendency"],onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.sandbox_reflex___state_hoteis____hotel_state.open_edit_hotel", ({ ["rid"] : h_rx_state_?.["rid"], ["nome"] : h_rx_state_?.["nome"] }), ({  })))], [_e], ({  })))),variant:"ghost"},"\u270f\ufe0f"),jsx(RadixThemesButton,{css:({ ["cursor"] : "pointer" }),disabled:h_rx_state_?.["has_pendency"],onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.sandbox_reflex___state_hoteis____hotel_state.delete_hotel", ({ ["rid"] : h_rx_state_?.["rid"], ["nome"] : h_rx_state_?.["nome"] }), ({  })))], [_e], ({  })))),variant:"ghost"},"\ud83d\uddd1\ufe0f")))))))
    )
});
